import csv
import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text  # Import text function


# Database connection parameters
host = 'tpcloudcomputing-415718:europe-west3:test-db'
dbname = 'postgres'
user = 'postgres'
password = 'vN`Y{N4H<7)g5BGb'
port = '5432'  # Default PostgreSQL port

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres using the Cloud SQL Python Connector package.
    """
    instance_connection_name = host  # e.g. 'project:region:instance'
    db_user = user  # e.g. 'my-db-user'
    db_pass = password  # e.g. 'my-db-password'
    db_name = dbname  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # Initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> sqlalchemy.engine.base.Connection:
        conn: sqlalchemy.engine.base.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy using the 'creator' argument to 'create_engine'
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return engine

# Connect to your PostgreSQL database
engine = connect_with_connector()

# Dictionary mapping file names to table names
files_to_tables = {
    'businesses.csv': 'business',
    'users.csv': 'user',
    'reviews.csv': 'review',
    'checkins.csv': 'checkin',
    'tips.csv': 'tip'
}

base_path = '/home/xjrr/fcul/cloud_computing/Project/cn-group03/yelp_dataset'

# Iterate through the dictionary and process each file-table pair
with engine.connect() as conn:
    metadata = MetaData()  # Correctly instantiate MetaData
    metadata.reflect(bind=engine)  # Reflect the database using the engine.
    for file_name, table_name in files_to_tables.items():
        full_path = os.path.join(base_path, file_name)
        table = Table(table_name, metadata, autoload_with=engine)  # Reflected table
        batch_data = []

        with open(full_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 0
            for row in reader:
                batch_data.append(row)
                counter += 1
                if len(batch_data) == 100:
                    conn.execute(table.insert(), batch_data)
                    batch_data = []
                    print(f"{counter} - 100 rows uploaded to {table_name}.")
                    conn.commit()

            if batch_data:  # Insert any remaining data
                conn.execute(table.insert(), batch_data)
                conn.commit()

          # Commit after each file's rows have been processed
        print(f"All data uploaded successfully to {table_name}.")

print("Data uploaded successfully.")

conn.close()  # Close the connection
