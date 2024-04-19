from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from urllib.parse import quote  
from sqlalchemy.engine import reflection



app = Flask(__name__)

# URL-encode the password
password_encoded = quote('vN`Y{N4H<7)g5BGb')

# Dynamically build the connection string using the encoded password
database_url = os.environ.get('DATABASE_URL', f'postgresql://postgres:{password_encoded}@34.107.119.237:5432/postgres')


app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'sslmode': 'require',
        'sslrootcert': 'cert/server-ca.pem',
        'sslcert': 'cert/client-cert.pem',
        'sslkey': 'cert/client-key.pem'
    }
}
db = SQLAlchemy(app)
print("Database URL:", database_url)
print("Database Engine Options:", app.config['SQLALCHEMY_ENGINE_OPTIONS'])

class Business(db.Model):
    __tablename__ = 'business'
    business_id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    postal_code = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stars = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    is_open = db.Column(db.Integer)

    def to_dict(self):
        return {
            'business_id': self.business_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'stars': self.stars,
            'review_count': self.review_count,
            'is_open': self.is_open
        }

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/businesses/<business_id>', methods=['GET'])
def get_business(business_id):
    business = Business.query.get(business_id)
    if business:
        return jsonify(business.to_dict())
    else:
        return jsonify({'error': 'Business not found'}), 404

@app.route('/businesses/top-rated', methods=['GET'])
def get_top_rated_businesses():
    city = request.args.get('city')
    limit = request.args.get('limit', 10, type=int)  # Default is 10, can be changed by the user

    if not city:
        return jsonify({'error': 'City is required'}), 400

    top_rated = Business.query.filter(Business.city == city).order_by(
        Business.stars.desc(), Business.review_count.desc()
    ).limit(limit).all()

    return jsonify([business.to_dict() for business in top_rated])


def print_database_tables():
    # Create an inspector object to inspect the database
    inspector = reflection.Inspector.from_engine(db.engine)
    # Retrieve and print the list of table names
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
