import logging
from functools import wraps
import connexion
from flask_cors import CORS
from flask import jsonify, request
from prometheus_client import start_http_server, Summary, Counter, generate_latest
from prometheus_client.core import CollectorRegistry
from os import environ as env
from urllib.parse import quote_plus, urlencode

from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

from pymongo import MongoClient
from flask import Flask, request, jsonify

#from api.auth.validator import Auth0JWTBearerTokenValidator
#from validator import Auth0JWTBearerTokenValidator

import validator as validator

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Total count of requests')

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
    

# Expose metrics endpoint
@app.app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    return generate_latest(registry)

# Example endpoint with Prometheus metrics
@app.app.route('/process')
@REQUEST_TIME.time()
@REQUEST_COUNT.count_exceptions()
def process_request():
    """A dummy function that takes some time."""
    time.sleep(random.random())
    return "Processed"


if __name__ == "__main__":
        # Start up the server to expose the metrics.
    start_http_server(9090)
    app.run(host='0.0.0.0', port=8000)
