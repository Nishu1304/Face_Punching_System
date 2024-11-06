from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Status(db.Model):
    __tablename__ = 'status'
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), primary_key=True)
    in_out_status = db.Column(db.Boolean, default=False)  # 0 for checked out, 1 for checked in
    check_in_time = db.Column(db.DateTime)

    def __init__(self, employee_id, in_out_status, check_in_time=None):
        self.employee_id = employee_id
        self.in_out_status = in_out_status
        self.check_in_time = check_in_time

    def __repr__(self):
        return f"<Status(employee_id={self.employee_id}, in_out_status={self.in_out_status}, check_in_time={self.check_in_time})>"


def update_attendance(employee_id, cluster_id):
    # Map cluster_id to employee_id based on cluster_mapping
    cluster_mapping = {
        1: 1,  # Aditya
        5: 2,  # Nishanka
        2: 3,  # Sonu
        0: 4,  # Pranav
        4: 5,  # Pranjal
        3: 6  # Vijaykrishna
    }

    # Get the actual employee ID based on cluster_id
    mapped_employee_id = cluster_mapping.get(cluster_id)

    if mapped_employee_id:
        # Check if the employee is already checked in
        current_status = Status.query.get(mapped_employee_id)
        if current_status:
            if current_status.in_out_status:  # Currently checked in
                # Check out the employee
                current_status.in_out_status = False
                current_status.check_in_time = datetime.utcnow()  # Record check-out time
            else:  # Currently checked out
                # Check in the employee
                current_status.in_out_status = True
                current_status.check_in_time = datetime.utcnow()  # Record check-in time
        else:
            # Create a new Status record if it doesn't exist
            new_status = Status(employee_id=mapped_employee_id, in_out_status=True, check_in_time=datetime.utcnow())
            db.session.add(new_status)

        db.session.commit()

    return mapped_employee_id
