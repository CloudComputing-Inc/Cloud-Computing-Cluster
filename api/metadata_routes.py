from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import certifi

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

#  cluster connection strings 
clusters = {
    # "Automotive": "mongodb+srv://" + up0 +"@cluster0.0zctiyc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "Books": "mongodb+srv://" + up2 +"@cluster0.ica6ojz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    # TO DO THE REST
}

def get_cluster_connection_string(category):
    # Mapping categories to cluster -> assumes each category is exclusively in one cluster.
    # Adjust more
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
