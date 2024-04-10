import json
import sqlite3


def debug_json_file(filename):
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error in line {line_number}: {e}")
                print(f"Problematic line content: {line}")
                break  # Stop after finding the first error

debug_json_file('yelp_academic_dataset_review.json')

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        # Read lines and parse each one as a JSON object
        return [json.loads(line) for line in file]

# businesses = load_json_data('yelp_academic_dataset_business.json')
# reviews = load_json_data('yelp_academic_dataset_review.json')
# users = load_json_data('yelp_academic_dataset_user.json')
# checkins = load_json_data('yelp_academic_dataset_checkin.json')
# tips = load_json_data('yelp_academic_dataset_tip.json')

# Connect to SQLite database
conn = sqlite3.connect('yelp_dataset.db')
cur = conn.cursor()

# Create tables
def create_tables():
    # Business table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS business (
        business_id TEXT PRIMARY KEY,
        name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        latitude REAL,
        longitude REAL,
        stars REAL,
        review_count INTEGER,
        is_open INTEGER
    )
    ''')

    # Review table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS review (
        review_id TEXT PRIMARY KEY,
        user_id TEXT,
        business_id TEXT,
        stars INTEGER,
        date TEXT,
        text TEXT,
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        FOREIGN KEY (business_id) REFERENCES business (business_id)
    )
    ''')

    # User table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS user (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        review_count INTEGER,
        yelping_since TEXT,
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        fans INTEGER,
        average_stars REAL,
        compliment_hot INTEGER,
        compliment_more INTEGER,
        compliment_profile INTEGER,
        compliment_cute INTEGER,
        compliment_list INTEGER,
        compliment_note INTEGER,
        compliment_plain INTEGER,
        compliment_cool INTEGER,
        compliment_funny INTEGER,
        compliment_writer INTEGER,
        compliment_photos INTEGER
    )
    ''')

    # Checkin table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS checkin (
        checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id TEXT,
        date TEXT,
        FOREIGN KEY (business_id) REFERENCES business (business_id)
    )
    ''')

    # Tip table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tip (
        tip_id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        date TEXT,
        compliment_count INTEGER,
        business_id TEXT,
        user_id TEXT,
        FOREIGN KEY (business_id) REFERENCES business (business_id),
        FOREIGN KEY (user_id) REFERENCES user (user_id)
    )
    ''')

    conn.commit()

create_tables()


def insert_business_data(businesses):
    for business in businesses:
        cur.execute('''
        INSERT INTO business (business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            business['business_id'],
            business['name'],
            business['address'],
            business['city'],
            business['state'],
            business.get('postal code'),  # Remember to use get for potentially missing data.
            business['latitude'],
            business['longitude'],
            business['stars'],
            business['review_count'],
            business['is_open']
        ))
    conn.commit()

def insert_review_data(reviews):
    for review in reviews:
        cur.execute('''
        INSERT INTO review (review_id, user_id, business_id, stars, date, text, useful, funny, cool)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            review['review_id'],
            review['user_id'],
            review['business_id'],
            review['stars'],
            review['date'],
            review['text'],
            review['useful'],
            review['funny'],
            review['cool']
        ))
    conn.commit()

def insert_user_data(users):
    for user in users:
        cur.execute('''
        INSERT INTO user (user_id, name, review_count, yelping_since, useful, funny, cool, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user['user_id'],
            user['name'],
            user['review_count'],
            user['yelping_since'],
            user['useful'],
            user['funny'],
            user['cool'],
            user['fans'],
            user['average_stars'],
            user['compliment_hot'],
            user['compliment_more'],
            user['compliment_profile'],
            user['compliment_cute'],
            user['compliment_list'],
            user['compliment_note'],
            user['compliment_plain'],
            user['compliment_cool'],
            user['compliment_funny'],
            user['compliment_writer'],
            user['compliment_photos']
        ))
    conn.commit()

def insert_checkin_data(checkins):
    for checkin in checkins:
        cur.execute('''
        INSERT INTO checkin (business_id, date)
        VALUES (?, ?)
        ''', (
            checkin['business_id'],
            checkin['date']  # This is a comma-separated list of timestamps.
        ))
    conn.commit()

def insert_tip_data(tips):
    for tip in tips:
        cur.execute('''
        INSERT INTO tip (text, date, compliment_count, business_id, user_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            tip['text'],
            tip['date'],
            tip['compliment_count'],
            tip['business_id'],
            tip['user_id']
        ))
    conn.commit()
businesses = load_json_data('yelp_academic_dataset_business.json')
insert_business_data(businesses) 
del businesses
reviews = load_json_data('yelp_academic_dataset_review.json')
insert_review_data(reviews)
del reviews
users = load_json_data('yelp_academic_dataset_user.json')
insert_user_data(users)
del users
# insert_checkin_data(checkins)
# insert_tip_data(tips)

conn.close()
