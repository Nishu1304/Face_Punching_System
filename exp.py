from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'mysql+pymysql://root:password@localhost/attendance'


engine = create_engine(DATABASE_URL)


Session = sessionmaker(bind=engine)
session = Session()

try:
    
    connection = engine.connect()
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    
    if 'connection' in locals(): 
        connection.close()


