import connexion
import grpc
import question_analysis_pb2
import question_analysis_pb2_grcp
from pymongo import MongoClient
from flask import Flask, request, jsonify

'''

app = Flask(__name__)

# Connect to MongoDB
user = "exampleuser"
password = "Ra2lMTHV3KmzBaGM"
up = user + ":" + password
client = MongoClient("mongodb+srv://"+up+"@single_qna.mongodb.net/Qna?retryWrites=true&w=majority")
db = client["database"]
collection = db["qna"]

# gRPC stub initialization
channel = grpc.insecure_channel('[::]:50055')
stub = question_analysis_pb2_grcp.LanguageAnalysisServiceStub(channel)

# Define endpoints for gRPC service functions
@app.route('/get_string_answer', methods=['POST'])
def get_string_answer():
    request_data = request.json
    response = stub.GetStringAnswer(question_analysis_pb2.GetStringAnswerRequest(**request_data))
    return jsonify(response.qAndA)

@app.route('/get_product_product_answer', methods=['POST'])
def get_product_product_answer():
    request_data = request.json
    response = stub.GetProductProductAnswer(question_analysis_pb2.GetProductProductAnswerRequest(**request_data))
    return jsonify(response.qAndA)

@app.route('/get_answer_type', methods=['POST'])
def get_answer_type():
    request_data = request.json
    response = stub.GetAnswerType(question_analysis_pb2.GetAnswerTypeRequest(**request_data))
    return jsonify(response.qAndA)

@app.route('/get_question_type', methods=['POST'])
def get_question_type():
    request_data = request.json
    response = stub.GetQuestionType(question_analysis_pb2.GetQuestionTypeRequest(**request_data))
    return jsonify(response.qAndA)

@app.route('/get_time_of_answer', methods=['POST'])
def get_time_of_answer():
    request_data = request.json
    response = stub.GetTimeOfAnswer(question_analysis_pb2.GetTimeOfAnswerRequest(**request_data))
    return jsonify(response.qAndA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    '''

# Create a Flask app with connexion
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

# Enable CORS
app.app.config['CORS_HEADERS'] = 'Content-Type'

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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
