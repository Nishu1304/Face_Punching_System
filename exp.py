from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URL
DATABASE_URL = 'mysql+pymysql://root:password@localhost/attendance'

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Your database operations go here
    connection = engine.connect()
    # Perform database operations using the connection
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection if it was opened
    if 'connection' in locals():  # Ensure connection is defined
        connection.close()


