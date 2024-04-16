from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/yelp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
