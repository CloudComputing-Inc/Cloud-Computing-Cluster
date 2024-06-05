from flask import Flask, jsonify, request, Response
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient, errors as pymongo_errors
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, generate_latest, push_to_gateway
import re
import os
import yaml
import time
import psutil

app = Flask(__name__)

# Prometheus metrics setup
registry = CollectorRegistry()
cpu_usage = Gauge('cpu_usage', 'CPU usage percentage', registry=registry)
memory_usage = Gauge('memory_usage', 'Memory usage in bytes', registry=registry)
request_latency = Histogram('request_latency_seconds', 'Request latency in seconds', registry=registry)
request_count = Counter('request_count', 'Total number of requests', registry=registry)
error_count = Counter('error_count', 'Total number of errors', registry=registry)

# Swagger UI configuration
SWAGGER_URL = '/api'
API_URL = './static/swagger.yml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask Market-Analysis API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Connect to MongoDB
user = "br"
password0 = "e3wmnqdtsYSEwa3I"
up0 = user + ":" + password0

password2 = "C7Kv49l3cZcS5NDo"
up2 = user + ":" + password2

password3 = "qVEqmdKYmrZoNlFw"
up3 = user + ":" + password3

password4 = "B0yEjiRW3P71vCkQ"
up4 = user + ":" + password4

# MongoDB clusters connection strings
clusters = {
    "cluster1": "mongodb+srv://" + up0 +"@cluster0.0zctiyc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster2": "mongodb+srv://" + up2 +"@cluster0.ica6ojz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster3": "mongodb+srv://" + up3 + "@cluster0.hv5qtwc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "cluster4":"mongodb+srv://" + up4 + "@cluster0.cymhfm5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
}

def get_cluster_connection_string(category):
    if category == "Automotive" or category == "All_Beauty" or category == "AMAZON_FASHION" or category == "Arts_Crafts_and_Sewing":
        return clusters["cluster1"]
    elif category == "Books" or category == "CDs_and_Vinyl" or category == "Cell_Phones_and_Accessories" or category == "Clothing_Shoes_and_Jewelry" or category == "Digital_Music":
        return clusters["cluster2"]
    elif category == "Electronics" or category == "Home_and_Kitchen" or category == "Movies_and_TV" or category == "Patio_Lawn_and_Garden" or category == "Pet_Supplies":
        return clusters["cluster3"]
    elif category == "Sports_and_Outdoors" or category == "Software" or category == "Tools_and_Home_Improvement" or category == "Toys_and_Games" or category == "Video_Games":
        return clusters["cluster4"]
    
    raise ValueError("Category not handled by any cluster")

@app.route('/', methods=['GET'])
def api_docs():
    with open(os.path.join(app.root_path, 'static', 'swagger.yaml'), 'r') as yaml_file:
        swagger_yaml_content = yaml.safe_load(yaml_file)
    return jsonify(swagger_yaml_content)

@app.route('/metadata', methods=['GET'])
def get_metadata():
    start_time = time.time()
    request_count.inc()
    category = request.args.get('category')
    brand = request.args.get('brand', None)
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if not category:
        error_count.inc()
        return jsonify({"error": "Category parameter is required."}), 400

    try:
        cluster_connection_string = get_cluster_connection_string(category)
    except ValueError:
        error_count.inc()
        return jsonify({"error": "Category not found or not supported."}), 404

    try:
        query = {'main_cat': category}
        if brand:
            query['brand'] = brand
        if min_price:
            min_price = float(min_price)
            query['price'] = {'$gte': f"${min_price:.2f}"}
        if max_price:
            max_price = float(max_price)
            query.setdefault('price', {})['$lte'] = f"${max_price:.2f}"

        client = MongoClient(cluster_connection_string)
        db = client['amazon_metadata']
        collection = db['metadata']
        products = collection.find(query, {'_id': 0, 'title': 1, 'brand': 1, 'price': 1})
        result = list(products)
        duration = time.time() - start_time
        request_latency.observe(duration)
        push_to_gateway('pushgateway:9091', job='market_analysis', registry=registry)
        return jsonify(result)
    except ValueError:
        error_count.inc()
        return jsonify({"error": "Invalid price format."}), 400
    except pymongo_errors.ConnectionError as e:
        error_count.inc()
        return jsonify({"error": "Database connection error."}), 500
    except Exception as e:
        error_count.inc()
        return jsonify({"error": str(e)}), 500

@app.route('/categories', methods=['GET'])
def get_main_categories():
    request_count.inc()
    start_time = time.time()
    main_categories = set()
    try:
        for cluster_connection_string in clusters.values():
            client = MongoClient(cluster_connection_string)
            db = client['amazon_metadata']
            collection = db['metadata']
            pipeline = [
                {
                    "$project": {
                        "main_cat_adjusted": {
                            "$cond": {
                                "if": {"$or": [
                                    {"$and": [
                                        {"$isArray": "$category"},
                                        {"$ne": [{"$arrayElemAt": ["$category", 0]}, "$main_cat"]}
                                    ]},
                                    {"$and": [
                                        {"$not": {"$isArray": "$category"}},
                                        {"$ne": ["$category", "$main_cat"]}
                                    ]}
                                ]},
                                "then": {"$cond": {"if": {"$isArray": "$category"}, "then": {"$arrayElemAt": ["$category", 0]}, "else": "$category"}},
                                "else": "$main_cat"
                            }
                        }
                    }
                },
                {"$match": {"main_cat_adjusted": {"$ne": None}}},
                {"$group": {"_id": "$main_cat_adjusted"}}
            ]

            categories = collection.aggregate(pipeline)
            for category in categories:
                cleaned_category = re.sub(r'<[^>]+>', '', category["_id"])
                main_categories.add(cleaned_category)
    except pymongo_errors.ConnectionError as e:
        error_count.inc()
        return jsonify({"error": "Database connection error."}), 500
    except Exception as e:
        error_count.inc()
        return jsonify({"error": str(e)}), 500

    duration = time.time() - start_time
    request_latency.observe(duration)
    push_to_gateway('pushgateway:9091', job='market_analysis', registry=registry)
    return jsonify({"main_categories": list(main_categories)})

@app.route('/top-products', methods=['GET'])
def get_top_products():
    start_time = time.time()
    request_count.inc()
    category = request.args.get('category')

    if not category:
        error_count.inc()
        return jsonify({"error": "Category parameter is required."}), 400

    try:
        cluster_connection_string = get_cluster_connection_string(category)
    except ValueError:
        error_count.inc()
        return jsonify({"error": "Category not found or not supported."}), 404

    try:
        client = MongoClient(cluster_connection_string)
        db = client['amazon_metadata']
        collection = db['metadata']
        projection = {'_id': 0, 'title': 1, 'brand': 1, 'price': 1}
        top_products = collection.find({"main_cat": category}, projection).sort("rank", 1).limit(2)
        result = list(top_products)
        duration = time.time() - start_time
        request_latency.observe(duration)
        push_to_gateway('pushgateway:9091', job='market_analysis', registry=registry)
        if len(result) == 2:
            return jsonify(result)
        elif result:
            return jsonify(result)
        else:
            error_count.inc()
            return jsonify({"error": "No top products found for the category."}), 404
    except pymongo_errors.ConnectionError as e:
        error_count.inc()
        return jsonify({"error": "Database connection error."}), 500
    except Exception as e:
        error_count.inc()
        return jsonify({"error": str(e)}), 500

@app.route('/top-brand', methods=['GET'])
def get_top_brand():
    start_time = time.time()
    request_count.inc()
    category = request.args.get('category')

    if not category:
        error_count.inc()
        return jsonify({"error": "Category parameter is required."}), 400

    try:
        cluster_connection_string = get_cluster_connection_string(category)
    except ValueError:
        error_count.inc()
        return jsonify({"error": "Category not found or not supported."}), 404

    try:
        client = MongoClient(cluster_connection_string)
        db = client['amazon_metadata']
        collection = db['metadata']
        top_brand = collection.aggregate([
            {
                "$match": {
                    "main_cat": category,
                    "brand": {"$exists": True, "$ne": ""}
                }
            },
            {
                "$group": {
                    "_id": "$brand",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ])
        
        top_brand_list = list(top_brand)
        duration = time.time() - start_time
        request_latency.observe(duration)
        push_to_gateway('pushgateway:9091', job='market_analysis', registry=registry)
        if top_brand_list and top_brand_list[0]['_id']:
            return jsonify({"top_brand": top_brand_list[0]['_id'], "count": top_brand_list[0]['count']})
        else:
            error_count.inc()
            return jsonify({"error": "No data found for the category."}), 404
    except pymongo_errors.ConnectionError as e:
        error_count.inc()
        return jsonify({"error": "Database connection error."}), 500
    except Exception as e:
        error_count.inc()
        return jsonify({"error": str(e)}), 500

@app.route('/metrics')
def metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().used)
    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50053)
