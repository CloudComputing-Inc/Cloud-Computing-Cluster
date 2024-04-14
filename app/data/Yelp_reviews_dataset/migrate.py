import csv
import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
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
    for file_name, table_name in files_to_tables.items():
        full_path = os.path.join(base_path, file_name)
        with open(full_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            batch_count = 0
            for row in reader:
                columns = ', '.join([f'"{column}"' for column in row.keys()])
                values = ', '.join([f"'{v.replace("'", "''")}'" for v in row.values()])  # Handle single quote in values
                query = f"INSERT INTO \"{table_name}\" ({columns}) VALUES ({values});"
                conn.execute(text(query))  # Execute the query safely using text function
                batch_count += 1

                if batch_count % 100 == 0:  # Check if batch_count is a multiple of 100
                    print(f"{batch_count} - {file_name} - {table_name} - {query}")
                    conn.commit()  # Commit the transaction
                    print(f"+ 100 rows committed to {table_name}")
            
            conn.commit()  # Commit any remaining transactions
            print(f"All data uploaded successfully to {table_name}.")

print("Data uploaded successfully.")

conn.close()  # Close the connection
