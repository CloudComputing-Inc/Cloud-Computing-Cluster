from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient
import re  # Regular expression operations
import os
import yaml
from concurrent import futures

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

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# connect to MongoDB, change the user and passwordX  to reflect your own clusters  connection strings
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
    #  return the appropriate cluster connection string
    if category == "Automotive" or category=="All_Beauty" or category=="AMAZON_FASHION" or category=="Arts_Crafts_and_Sewing" :
        return clusters["cluster1"]
    elif category == "Books" or  category == "CDs_and_Vinyl" or category == "Cell_Phones_and_Accessories" or category == "Clothing_Shoes_and_Jewelry" or  category == "Digital_Music":
        return clusters["cluster2"]
    elif category == "Electronics" or  category == "Home_and_Kitchen" or category == "Movies_and_TV" or category == "Patio_Lawn_and_Garden" or  category == "Pet_Supplies":
        return clusters["cluster3"]
    elif category == "Sports_and_Outdoors" or  category == "Software" or category == "Tools_and_Home_Improvement" or  category == "Toys_and_Games" or  category == "Video_Games":
        return clusters["cluster4"]
    
    # If category does not match, raise an exception 
    raise ValueError("Category not handled by any cluster")

# MongoDB connection setup
def get_cluster_connection_string(category):
    user = "br"
    passwords = {
        "cluster1": "e3wmnqdtsYSEwa3I",
        "cluster2": "C7Kv49l3cZcS5NDo",
        "cluster3": "qVEqmdKYmrZoNlFw",
        "cluster4": "B0yEjiRW3P71vCkQ"
    }
    clusters = {
        "cluster1": f"mongodb+srv://{user}:{passwords['cluster1']}@cluster0.0zctiyc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        # Add similar lines for other clusters
    }
    # Logic to select the correct cluster based on category
    return clusters["cluster1"]  # Simplified example

@app.route('/', methods=['GET'])
def api_docs():
    # Load the YAML file
    with open(os.path.join(app.root_path, 'static', 'swagger.yaml'), 'r') as yaml_file:
        swagger_yaml_content = yaml.safe_load(yaml_file)

    # Convert YAML content to JSON and return as JSON response
    return jsonify(swagger_yaml_content)

@app.route('/metadata', methods=['GET'])
def get_metadata():
    category = request.args.get('category')
    brand = request.args.get('brand', None)
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if not category:
        return jsonify({"error": "Category parameter is required."}), 400

    try:
        cluster_connection_string = get_cluster_connection_string(category)
        if not cluster_connection_string:
            return jsonify({"error": "Category not found or not supported."}), 404

        # Use main_cat instead of category, based on your MongoDB objects
        query = {'main_cat': category}
        
        # Add brand to query if provided
        if brand:
            query['brand'] = brand

        # Modify the price filter to handle string values
        if min_price:
            min_price = float(min_price)
            # Convert string price to number before comparison
            query['price'] = {'$gte': f"${min_price:.2f}"}
        if max_price:
            max_price = float(max_price)
            # Ensure the price field exists in the query before updating it
            query.setdefault('price', {})['$lte'] = f"${max_price:.2f}"

        client = MongoClient(cluster_connection_string)
        db = client['amazon_metadata']
        collection = db['metadata']
        
        products = collection.find(query, {'_id': 0, 'title': 1, 'brand': 1, 'price': 1})
        result = list(products)
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "Invalid price format."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/categories', methods=['GET'])
def get_main_categories():
    main_categories = set()  # Use a set to avoid duplicates
    # Assuming 'clusters' dictionary is defined with your MongoDB cluster connection strings
    for cluster_connection_string in clusters.values():
        client = MongoClient(cluster_connection_string)
        db = client['amazon_metadata']
        collection = db['metadata']

        # MongoDB pipeline to adjust the category names and remove HTML tags
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
            {"$match": {"main_cat_adjusted": {"$ne": None}}},  # Filter out documents where main_cat_adjusted is null
            {"$group": {"_id": "$main_cat_adjusted"}}
        ]

        categories = collection.aggregate(pipeline)
        for category in categories:
            cleaned_category = re.sub(r'<[^>]+>', '', category["_id"])  # Remove HTML tags
            main_categories.add(cleaned_category)

    return jsonify({"main_categories": list(main_categories)})

@app.route('/top-products', methods=['GET'])
def get_top_products():
    category = request.args.get('category')
    cluster_connection_string = get_cluster_connection_string(category)
    
    # Check if the cluster connection string is valid
    if not cluster_connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404

    client = MongoClient(cluster_connection_string)
    db = client['amazon_metadata']
    collection = db['metadata']
    
    # Define the projection to only include title, brand, and price, excluding MongoDB's default _id
    projection = {'_id': 0, 'title': 1, 'brand': 1, 'price': 1}
    
    # Querying the top 2 products sorted by rank
    top_products = collection.find({"main_cat": category}, projection).sort("rank", 1).limit(2)
    
    # Convert the cursor to a list and check the length of the list
    result = list(top_products)
    if len(result) == 2:
        # Return only the top 2 products as a list
        return jsonify(result)
    elif result:
        # If there is less than 2 products, return whatever is available
        return jsonify(result)
    else:
        # No products found for the category
        return jsonify({"error": "No top products found for the category."}), 404

@app.route('/top-brand', methods=['GET'])
def get_top_brand():
    category = request.args.get('category')
    cluster_connection_string = get_cluster_connection_string(category)
    
    # Check if the cluster connection string is valid (assumes get_cluster_connection_string returns None if not valid)
    if not cluster_connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404

    client = MongoClient(cluster_connection_string)
    db = client['amazon_metadata']
    collection = db['metadata']

    # MongoDB aggregation to find the brand with the most products, ensuring the brand is not null or empty
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
    if top_brand_list and top_brand_list[0]['_id']:
        return jsonify({"top_brand": top_brand_list[0]['_id'], "count": top_brand_list[0]['count']})
    else:
        return jsonify({"error": "No data found for the category."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50053)
