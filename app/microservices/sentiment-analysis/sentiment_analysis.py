from concurrent import futures
import grpc
import reviews_pb2
import reviews_pb2_grpc
from google.cloud import bigquery
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import os
import yaml
from urllib.parse import quote  
from sqlalchemy.engine import reflection

project_id = 'cloudcomputinginc'

dataset = 'electronics'
table = 'data'

table_id = f"{project_id}.{dataset}.{table}"  # Update with your BigQuery table ID

app = Flask(__name__)

# Swagger UI setup
SWAGGER_URL = '/api'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "BigQuery CRUD API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Initialize BigQuery client
bigquery_client = bigquery.Client()

@app.route('/api/v1/items', methods=['GET'])
def get_items():
    query = f"SELECT * FROM `{table_id}`"
    query_job = bigquery_client.query(query)
    rows = query_job.result()
    items = [dict(row) for row in rows]
    return jsonify(items), 200

@app.route('/api/v1/items', methods=['POST'])
def create_item():
    data = request.json
    row = {
        "verified_purchase": data['verified_purchase'],
        "timestamp": data['timestamp'],
        "helpful_vote": data['helpful_vote'],
        "user_id": data['user_id'],
        "asin": data['asin'],
        "parent_asin": data['parent_asin'],
        "rating": data['rating'],
        "text": data['text'],
        "title": data['title']
    }
    errors = bigquery_client.insert_rows_json(table_id, [row])
    if errors:
        return jsonify({"error": str(errors)}), 500
    return jsonify(row), 201

@app.route('/api/v1/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    query = f"SELECT * FROM `{table_id}` WHERE asin = '{item_id}'"
    query_job = bigquery_client.query(query)
    rows = query_job.result()
    items = [dict(row) for row in rows]
    if items:
        return jsonify(items[0]), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/v1/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    query = f"""
        UPDATE `{table_id}`
        SET 
            verified_purchase = {data['verified_purchase']}, 
            timestamp = {data['timestamp']}, 
            helpful_vote = {data['helpful_vote']},
            user_id = '{data['user_id']}', 
            parent_asin = '{data['parent_asin']}', 
            rating = {data['rating']}, 
            text = '{data['text']}', 
            title = '{data['title']}'
        WHERE asin = '{item_id}'
    """
    query_job = bigquery_client.query(query)
    query_job.result()
    return jsonify(data), 200

@app.route('/api/v1/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    query = f"DELETE FROM `{table_id}` WHERE asin = '{item_id}'"
    query_job = bigquery_client.query(query)
    query_job.result()
    return '', 204

@app.route('/static/<path:path>', methods=['GET'])
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50056)
