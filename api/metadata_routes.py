from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import certifi

# connect to MongoDB, change the user and passwordX  to reflect your own clusters  connection strings
user = "br"
password0 = "e3wmnqdtsYSEwa3I"
up0 = user + ":" + password0
cluster0 = "mongodb+srv://" + up0 +"@cluster0.0zctiyc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

password2 = "C7Kv49l3cZcS5NDo"
up2 = user + ":" + password2
cluster2 = "mongodb+srv://" + up2 +"@cluster0.ica6ojz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

password3 = "qVEqmdKYmrZoNlFw"
up3 = user + ":" + password3
cluster3 = "mongodb+srv://" + up3 + "@cluster0.hv5qtwc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

password4 = "B0yEjiRW3P71vCkQ"
up4 = user + ":" + password4 
cluster4 = "mongodb+srv://" + up4 + "@cluster0.cymhfm5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

#  cluster connection strings 
clusters = {
    "Automotive": cluster0,
    "All_Beauty": cluster0,
    "AMAZON_FASHION": cluster0,
    "Arts_Crafts_and_Sewing": cluster0,

    "Books": cluster2,
    "CDs_and_Vinyl": cluster2,
    "Cell_Phones_and_Accessories": cluster2,
    "Clothing_Shoes_and_Jewelry": cluster2,
    "Digital_Music": cluster2,

    "Electronics": cluster3,
    "Home_and_Kitchen": cluster3,
    "Movies_and_TV": cluster3,
    "Patio_Lawn_and_Garden": cluster3,
    "Pet_Supplies": cluster3,

    "Sports_and_Outdoors": cluster4,
    "Software": cluster4,
    "Tools_and_Home_Improvement": cluster4,
    "Toys_and_Games": cluster4,
    "Video_Games": cluster4,
}

def get_cluster_connection_string(category):
    # Mapping categories to cluster -> assumes each category is exclusively in one cluster.
    if category in clusters:
        return clusters[category]
    else:
        # Default or error handling
        return None
    
    
metadata_bp = Blueprint('metadata', __name__, url_prefix='/api/v1')

@metadata_bp.route('/metadata', methods=['GET'])
def get_metadata():
    category = request.args.get('category')
    brand = request.args.get('brand')
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)

    cluster_connection_string = get_cluster_connection_string(category)
    if not cluster_connection_string:
        return jsonify({"error": "Category not found or not supported."}), 404

    client = MongoClient(cluster_connection_string, tlsCAFile=certifi.where())
    db = client['amazon_metadata']  
    collection = db['metadata']

    # Construct the query
    query = {"category": category}
    if brand:
        query['brand'] = brand
    if min_price is not None or max_price is not None:
        query['price'] = {}
        if min_price is not None:
            query['price']['$gte'] = min_price
        if max_price is not None:
            query['price']['$lte'] = max_price

    documents = collection.find(query)

    response = [doc for doc in documents]
    for doc in response:
        doc.pop('_id', None)  # Remove MongoDB's '_id'

    return jsonify(response)

@metadata_bp.route('/categories', methods=['GET'])
def get_main_categories():
    client = MongoClient(clusters["Books"], tlsCAFile=certifi.where())  # Example using "Books" cluster
    db = client['amazon_metadata']
    collection = db['metadata']

    # MongoDB aggregation to get unique categories
    categories = collection.aggregate([
        {"$unwind": "$category"},
        {"$group": {"_id": None, "main_cats": {"$addToSet": "$main_cat"}}},
        {"$project": {"_id": 0, "main_cats": 1}}
    ])
    categories_list = list(categories)
    if categories_list:
        return jsonify({"main_categories": categories_list[0]['main_cats']})
    return jsonify({"main_categories": []})

@metadata_bp.route('/top-products', methods=['GET'])
def get_top_products():
    category = request.args.get('category')
    client = MongoClient(get_cluster_connection_string(category), tlsCAFile=certifi.where())
    db = client['amazon_metadata']
    collection = db['metadata']

    # We define the projection here. '1' means to include the field, '_id' is set to 0 to exclude it.
    projection = {'_id': 0, 'title': 1, 'brand': 1, 'price': 1}

    # Add the projection to the find method call
    top_products = collection.find({"main_cat": category}, projection).sort("rank", 1).limit(2)

    # The response now only includes the specified fields
    response = [doc for doc in top_products]

    return jsonify(response)


@metadata_bp.route('/top-brand', methods=['GET'])
def get_top_brand():
    category = request.args.get('category')
    client = MongoClient(get_cluster_connection_string(category), tlsCAFile=certifi.where())
    db = client['amazon_metadata']
    collection = db['metadata']

    # MongoDB aggregation to find the brand with the most products
    top_brand = collection.aggregate([
        {"$match": {"main_cat": category}},
        {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])
    top_brand_list = list(top_brand)
    if top_brand_list:
        return jsonify({"top_brand": top_brand_list[0]['_id'], "count": top_brand_list[0]['count']})
    return jsonify({"error": "No data found for the category."})


