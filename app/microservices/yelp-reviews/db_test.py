from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from urllib.parse import quote

# URL-encode your password
password_encoded = quote('vN`Y{N4H<7)g5BGb')

# Connection string with URL-encoded password
connection_string = f'postgresql://postgres:{password_encoded}@34.159.70.188:5432/postgres'
print("Connection string:", connection_string)
engine = create_engine(connection_string, connect_args={
    'sslmode': 'require',
    'sslrootcert': 'cert/server-ca.pem',
    'sslcert': 'cert/client-cert.pem',
    'sslkey': 'cert/client-key.pem'
})

try:
    # Connect to the database
    conn = engine.connect()
    print("Connected successfully.")

    # Create an inspector object to inspect the database
    inspector = reflection.Inspector.from_engine(engine)

    # Retrieve and print the list of table names
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)

    # Close the connection
    conn.close()
except Exception as e:
    print("Error connecting to the database:", e)
