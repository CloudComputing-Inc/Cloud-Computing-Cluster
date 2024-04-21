from functools import wraps
import connexion
from flask_cors import CORS
from flask import jsonify, request

from os import environ as env
from urllib.parse import quote_plus, urlencode

#from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

from pymongo import MongoClient
from flask import Flask, request, jsonify
#from authlib.integrations.flask_oauth2 import ResourceProtector
#from api.auth.validator import Auth0JWTBearerTokenValidator
#from validator import Auth0JWTBearerTokenValidator
import validator as validator
'''
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY") #e61de153fb483642f1ca67954343cd05aef81184c290a3b8201a1136adfe8379

oauth = OAuth(app)

#TODO urls

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# Initialize ResourceProtector and Auth0JWTBearerTokenValidator
require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    env.get("AUTH0_DOMAIN"),
    "https:\\amazon-reviews.net" 
)
require_auth.register_token_validator(validator)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )'''

# Define the authenticate decorator
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the request contains a valid token
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({"error": "Authorization token is missing"}), 401

        # Validate the token
        valid, _ = validator.validate_token(token)
        if not valid:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function

# Define the authorize decorator
def authorize(scope):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Perform authorization checks here
            if not has_permission(scope):
                return jsonify({'message': 'Insufficient permissions'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Define the has_permission function
def has_permission(permission):
    # Example authorization check (replace with actual logic)
    # Check if the user has the required permission in the token's scope
    token = request.headers.get('Authorization', None)
    _, claims = validator.validate_token(token)
    if not permission in claims.get('scope', '').split():
        return False
    return True

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

# Enable CORS
CORS(app.app)

# Define a route for the root URL
@app.app.route('/')
def welcome():
    response = {
        "Welcome": "Welcome to the Amazon Reviews Analyzer API!",
        "Note": "Please refer to the Swagger UI for more detailed information on each endpoint.",
        "Endpoints": {
            "/api/v1/categories": "Retrieve a list of product categories. No additional fields required.",
            "/api/v1/metadata?category={category}&brand={brand}&minPrice={minPrice}&maxPrice={maxPrice}": "Fetch metadata for products with optional filtering. Replace {category} with the product category (required), {brand} with the product brand (optional), {minPrice} with the minimum price (optional), {maxPrice} with the maximum price (optional).",
            "/api/v1/top-brand?category={category}": "Get the top brand in a specified category. Replace {category} with the product category (required).",
            "/api/v1/top-products?category={category}": "Retrieve top products in a category. Replace {category} with the product category (required)."
        }
    }
    return jsonify(response)


@app.route('/api/v1/top-products', methods=['POST'])
@authenticate
def get_top_products():
    request_data = request.json
    # Authorization check
    if not has_permission('read:top_products'):
        return jsonify({'message': 'Insufficient permissions'}), 403
    # Endpoint logic using the gRPC stub
    response = stub.GetTopProducts(market_performance_pb2.GetTopProductsRequest(**request_data))
    return jsonify(response)

@app.route('/api/v1/top-brand', methods=['POST'])
@authenticate
def get_top_brand():
    request_data = request.json
    # Authorization check
    if not has_permission('read:top_brand'):
        return jsonify({'message': 'Insufficient permissions'}), 403
    # Endpoint logic using the gRPC stub
    response = stub.GetTopBrand(market_performance_pb2.GetTopBrandRequest(**request_data))
    return jsonify(response)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
