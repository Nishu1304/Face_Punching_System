import os
import joblib
import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from flask import Flask, render_template, Response, flash, redirect, url_for
from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from status import Status, db
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLAlchemy Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/attendance'  # Update this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Define the Attendance model
class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    score = db.Column(db.Boolean, default=False)  # True for checked in, False for checked out


# Define the Entries model
class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)
    hours_worked = db.Column(db.Float)
    late_arrival = db.Column(db.Boolean)


# Global variables for camera and models
camera = None
kmeans_model = None
mtcnn = None
inception_model = None

# Cluster mapping
cluster_mapping = {
    1: 1,  # Aditya
    5: 2,  # Nishanka
    2: 3,  # Sonu
    0: 4,  # Pranav
    4: 5,  # Pranjal
    3: 6  # Vijaykrishna
}


# Load KMeans model
def load_kmeans_model():
    model_path = 'kmeans_model.pkl'
    return joblib.load(model_path)


# Load MTCNN and InceptionResnetV1 for face detection and embeddings
def load_embedding_models():
    global mtcnn, inception_model
    mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')
    inception_model = InceptionResnetV1(pretrained='vggface2').eval().to('cuda' if torch.cuda.is_available() else 'cpu')


# Function to extract face embeddings from an image
def get_face_embeddings(image):
    boxes, _ = mtcnn.detect(image)
    print("Detected boxes:", boxes)  # Debugging line to check if faces are detected
    embeddings = []

    if boxes is not None:
        for box in boxes:
            face = image[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
            face = cv2.resize(face, (160, 160))
            face_tensor = torch.from_numpy(face).permute(2, 0, 1).float().unsqueeze(0) / 255.0
            face_tensor = face_tensor.to('cuda' if torch.cuda.is_available() else 'cpu')
            with torch.no_grad():
                embedding = inception_model(face_tensor)
            embeddings.append(embedding.cpu().numpy().flatten())
            print("Generated embedding:", embedding)  # Debugging line to check embeddings

    print("Total embeddings generated:", len(embeddings))  # Check the number of embeddings
    return np.array(embeddings)


# Attendance recording function using SQLAlchemy
def record_attendance(cluster_id):
    current_time = datetime.now()
    employee_id = cluster_mapping.get(cluster_id, None)

    print(f"Processing attendance for cluster_id: {cluster_id}, resolved employee_id: {employee_id}")

    if employee_id is not None:
        employee_status = Status.query.filter_by(employee_id=employee_id).first()
        print(f"Current employee status: {employee_status}")

        if employee_status is None:
            # First check-in
            new_status = Status(employee_id=employee_id, in_out_status=True, check_in_time=current_time)
            db.session.add(new_status)
            db.session.commit()
            print(f"Checked in for {employee_id} (first time).")
        else:
            if not employee_status.in_out_status:  # Check-in
                employee_status.in_out_status = True
                employee_status.check_in_time = current_time
                db.session.commit()
                print(f"Checked in for {employee_id}.")
            else:  # Check-out
                # Calculate hours worked
                hours_worked = (current_time - employee_status.check_in_time).total_seconds() / 3600
                late_arrival = employee_status.check_in_time.time() > time(9, 0)  # Late if after 9:00 AM

                # Insert an entry into the entries table
                new_entry = Entry(
                    employee_id=employee_id,
                    date=current_time.date(),
                    check_in=employee_status.check_in_time.time(),
                    check_out=current_time.time(),
                    hours_worked=hours_worked,
                    late_arrival=late_arrival
                )
                db.session.add(new_entry)

                # Reset status to checked out
                employee_status.in_out_status = False
                employee_status.check_in_time = None
                db.session.commit()
                print(f"Checked out and recorded attendance for {employee_id}.")
    else:
        print(f"Error: No employee found for cluster_id: {cluster_id}")


# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')


# Function to generate video frames for streaming
def gen_frames():
    global camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    global camera
    camera = cv2.VideoCapture(0)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture', methods=['POST'])
def capture():
    global camera
    success, frame = camera.read()

    if success:
        cv2.imwrite('static/captured_face.jpg', frame)
        face_embeddings = get_face_embeddings(frame)

        if face_embeddings.size > 0:
            cluster_label = kmeans_model.predict(face_embeddings)[0]  # Get single cluster label
            print("Predicted cluster:", cluster_label)  # Debugging line to check cluster prediction
            record_attendance(cluster_label)
            flash(
                f'Image captured and attendance recorded for employee ID {cluster_mapping.get(cluster_label, "Unknown")}.')  # Updated message
        else:
            flash('No face detected in the image. Please try again.')
    else:
        flash('Failed to capture image. Please try again.')

    return redirect(url_for('home'))


if __name__ == '__main__':
    kmeans_model = load_kmeans_model()  # Load the KMeans model once when the app starts
    load_embedding_models()  # Load the MTCNN and InceptionResnetV1 models once when the app starts

    # Create database tables within the application context
    with app.app_context():
        db.create_all()  # Creates tables if not already present

    app.run(debug=True)

