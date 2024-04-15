import csv
import os

# Dictionary mapping file names to table names
files_to_tables = {
    'businesses.csv': 'business',
    'reviews.csv': 'review',
    'users.csv': 'user',
    'checkins.csv': 'checkin',
    'tips.csv': 'tip'
}

base_path = '/home/xjrr/fcul/cloud_computing/Project/cn-group03/yelp_dataset'  # Path where your CSV files are located
output_path = '/home/xjrr/fcul/cloud_computing/Project/cn-group03/yelp_dataset'  # Path to save the SQL files

# Function to create SQL insert statement from CSV data
def create_sql_inserts(csv_path, table_name, output_file):
    with open(csv_path, newline='') as csvfile, open(output_file, 'w') as sqlfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            columns = ', '.join([f'"{column}"' for column in row.keys()])
            values = ', '.join([f"'{v.replace("'", "''")}'" for v in row.values()])
            sqlfile.write(f"INSERT INTO \"{table_name}\" ({columns}) VALUES ({values});\n")

# Iterate through the dictionary and process each file-table pair
for file_name, table_name in files_to_tables.items():
    csv_full_path = os.path.join(base_path, file_name)
    output_sql_file = os.path.join(output_path, f"{table_name}_inserts.sql")
    create_sql_inserts(csv_full_path, table_name, output_sql_file)
    print(f"SQL insert statements for {table_name} have been written to {output_sql_file}")
