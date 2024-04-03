import gzip
import json
import psycopg2
from psycopg2 import sql

def create_database(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if the database already exists
        cur.execute(
            sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"),
            [db_name]
        )
        exists = cur.fetchone()

        if not exists:
            # Create the new database
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

def create_table(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Create reviews table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                rating FLOAT,
                title TEXT,
                text TEXT,
                images JSONB,
                asin TEXT,
                parent_asin TEXT,
                user_id TEXT,
                timestamp TIMESTAMP,  -- Define timestamp column
                verified_purchase BOOLEAN,
                helpful_vote BIGINT
            )
        """)
        print("Table 'reviews' created successfully.")

    except Exception as e:
        print("Error creating table:", e)

    finally:
        cur.close()
        conn.close()

def sanitize_data(data):
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Remove or replace \x00 characters
            sanitized_value = value.replace('\x00', '')
            sanitized_data[key] = sanitized_value
        else:
            sanitized_data[key] = value
    return sanitized_data


def insert_data(db_name, user, password, host, port, json_lines_file):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        with gzip.open(json_lines_file, 'rt') as f:
            for line in f:
                data = json.loads(line.strip())
                # Sanitize the data to remove null characters
                sanitized_data = sanitize_data(data)
                # Convert Unix timestamp from milliseconds to seconds
                timestamp_seconds = sanitized_data.get('timestamp') / 1000.0
                # Insert sanitized data into the table with explicit typecasting to timestamp
                cur.execute("""
                    INSERT INTO reviews (rating, title, text, images, asin, parent_asin, user_id, timestamp, verified_purchase, helpful_vote)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s)
                """, (
                    sanitized_data.get('rating'),
                    sanitized_data.get('title'),
                    sanitized_data.get('text'),
                    json.dumps(sanitized_data.get('images')),
                    sanitized_data.get('asin'),
                    sanitized_data.get('parent_asin'),
                    sanitized_data.get('user_id'),
                    timestamp_seconds,  # Unix timestamp in seconds
                    sanitized_data.get('verified_purchase'),
                    sanitized_data.get('helpful_vote')
                ))

        print("Data inserted successfully.")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        conn.commit()
        cur.close()
        conn.close()


# Replace these values with your own
db_name = "reviews"
user = "chranama"
password = "password"
host = "localhost"  # Change if your PostgreSQL server is running on a different host
port = "5432"       # Change if your PostgreSQL server is running on a different port
json_lines_file = "data/Electronics.jsonl.gz"  # Provide the path to your JSON lines file

# Create the database and table
create_database(db_name, user, password, host, port)
create_table(db_name, user, password, host, port)

# Insert data into the table
insert_data(db_name, user, password, host, port, json_lines_file)


