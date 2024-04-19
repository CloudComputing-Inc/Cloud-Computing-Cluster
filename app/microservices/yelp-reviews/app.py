from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
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

# Swagger UI configuration
SWAGGER_URL = ''  # URL for exposing Swagger UI (without trailing '/')
API_URL = './static/swagger.yaml'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Flask Business API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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

@app.route('/static/swagger.yaml')
def swagger_yaml():
    print("Sending swagger.yaml")
    return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.yaml', as_attachment=False, mimetype='application/x-yaml')

@app.route('/states', methods=['GET'])
def list_states():
    states = db.session.query(Business.state).distinct().all()
    state_list = [state[0] for state in states]  # Unpack tuple results into a list
    return jsonify({'states': state_list})

@app.route('/cities', methods=['GET'])
def list_cities():
    cities = db.session.query(Business.city).distinct().all()
    city_list = [city[0] for city in cities]  # Unpack tuple results into a list
    return jsonify({'cities': city_list})

@app.route('/businesses', methods=['GET'])
def list_business_ids():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    offset = (page - 1) * limit
    
    business_info = Business.query.with_entities(Business.name, Business.business_id).order_by(Business.name).limit(limit).offset(offset).all()
    
    results = [{'name': info[0], 'id': info[1]} for info in business_info]
    
    return jsonify({
        'business_ids': results,
        'page': page,
        'limit': limit
    })

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
    state = request.args.get('state')
    limit = request.args.get('limit', 10, type=int)

    query = Business.query

    if city:
        query = query.filter(Business.city == city)
    if state:
        query = query.filter(Business.state == state)

    top_rated = query.order_by(Business.stars.desc(), Business.review_count.desc()).limit(limit).all()

    return jsonify([business.to_dict() for business in top_rated])


def print_database_tables():
    # Create an inspector object to inspect the database
    inspector = reflection.Inspector.from_engine(db.engine)
    # Retrieve and print the list of table names
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
