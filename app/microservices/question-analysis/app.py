from functools import wraps
import connexion
import grpc
import question_analysis_pb2
import question_analysis_pb2_grcp
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from authlib.integrations.flask_oauth2 import ResourceProtector
import os
import yaml
import re
#from api.auth.validator import Auth0JWTBearerTokenValidator
#from api.validator import Auth0JWTBearerTokenValidator

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/api'  # URL for exposing Swagger UI (without trailing '/')
API_URL = './static/swagger.yml'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Flask Market-Analysis API"
    },
)

# Connect to MongoDB
user = "exampleuser"
password = "Ra2lMTHV3KmzBaGM"
up = user + ":" + password
client = MongoClient("mongodb+srv://"+up+"@single_qna.mongodb.net/Qna?retryWrites=true&w=majority")
db = client["database"]
collection = db["qna"]

def get_connection_string():
    user = "exampleuser"
    password = "Ra2lMTHV3KmzBaGM"
    up = user + ":" + password
    connection = "mongodb+srv://"+up+"@single_qna.mongodb.net/Qna?retryWrites=true&w=majority"
    return connection


# gRPC stub initialization
#channel = grpc.insecure_channel('[::]:50055')
#stub = question_analysis_pb2_grcp.LanguageAnalysisServiceStub(channel)

'''
    validator = Auh0JWTBearerTokenValidator(
        "your-auth0-domain",
        "your-api-identifier"
    )
    require_auth = ResourceProtector()
require_auth.register_token_validator(validator)'''

# Define a route for the root URL
@app.route('/', methods=['GET']) 
def api_docs():
    with open(os.path.join(app.root_path, 'static', 'swagger.yaml'),'r') as yaml_file:
        swagger_yaml_content = yaml.safe_load(yaml_file)
    return jsonify(swagger_yaml_content)

# Define endpoints for gRPC service functions
@app.route('/get_string_answer', methods=['POST'])
def get_string_answer():
    asin = request.args.get('asin')
    question = request.args.get('question')
    connection_string = get_connection_string

    if not connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404
    client = MongoClient(connection_string)
    db = client["singleqna"]
    collection = db["qna"]

    query = {'product': asin}

    query['question'] = question

    
    answer = collection.find(query,{'answer':1})
    result = list(answer)
    return jsonify(result)





'''@app.route('/api/v1/get_string_answer', methods=['POST'])
#@authenticate
def get_string_answer():
    request_data = request.json
    response = stub.GetStringAnswer(question_analysis_pb2.GetStringAnswerRequest(**request_data))
    return jsonify(response.qAndA)'''

@app.route('/get_product_product_answer', methods=['POST'])
def get_product_product_answer():
    asin = request.args.get('asin')
    connection_string = get_connection_string

    if not connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404
    client = MongoClient(connection_string)
    db = client["singleqna"]
    collection = db["qna"]

    query = {'product': asin}

    answer = collection.find(query,{'asin':1 ,'answer':1})
    result = list(answer)
    return jsonify(result)

@app.route('/get_answer_type', methods=['POST'])
def get_answer_type():
    asin = request.args.get('asin')
    answer = request.args.get('answer')
    connection_string = get_connection_string

    if not connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404
    client = MongoClient(connection_string)
    db = client["singleqna"]
    collection = db["qna"]

    query = {'product': asin}

    query['answer'] = answer

    answer = collection.find(query,{'answerType':1})
    result = list(answer)
    return jsonify(result)

@app.route('/get_question_type', methods=['POST'])
def get_question_type():
    asin = request.args.get('asin')
    question = request.args.get('question')
    connection_string = get_connection_string

    if not connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404
    client = MongoClient(connection_string)
    db = client["singleqna"]
    collection = db["qna"]

    query = {'product': asin}

    query['question'] = question

    answer = collection.find(query,{'questionType':1})
    result = list(answer)
    return jsonify(result)

@app.route('/get_time_of_answer', methods=['POST'])
#@authenticate
def get_time_of_answer():
    asin = request.args.get('asin')
    question = request.args.get('question')
    connection_string = get_connection_string

    if not connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404
    client = MongoClient(connection_string)
    db = client["singleqna"]
    collection = db["qna"]

    query = {'product': asin}

    query['question'] = question

    answer = collection.find(query,{'answerTime':1})
    result = list(answer)
    return jsonify(result)
    

'''def authenticate(f):
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

def authorize(scope):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Perform authorization checks here
            if not has_permission(scope):
                return jsonify({'message': 'Insufficient permissions'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(permission):
    # Example authorization check (replace with actual logic)
    # Check if the user has the required permission in the token's scope
    token = request.headers.get('Authorization', None)
    _, claims = validator.validate_token(token)
    if not permission in claims.get('scope', '').split():
        return False
    return True'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

'''
# Create a Flask app with connexion
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

# Enable CORS
app.app.config['CORS_HEADERS'] = 'Content-Type'''

'''
# Define a route for the root URL
@app.route('/')
def welcome():
    response = {
        "Welcome": "Welcome to the gRPC and Swagger/OpenAPI integrated Flask application!",
        "Endpoints": {
            "/api/v1/get_string_answer": "Fetch string answers from gRPC service.",
            "/api/v1/get_product_product_answer": "Fetch product answers from gRPC service.",
            "/api/v1/get_answer_type": "Fetch answer types from gRPC service.",
            "/api/v1/get_question_type": "Fetch question types from gRPC service.",
            "/api/v1/get_time_of_answer": "Fetch answer times from gRPC service."
        }
    }
    return jsonify(response)
'''

