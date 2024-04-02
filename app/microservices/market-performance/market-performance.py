import grpc
import market_performance_pb2
import market_performance_pb2_grpc
from pymongo import MongoClient
from concurrent import futures

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

class MarketPerformanceService(market_performance_pb2_grpc.MarketPerformanceServiceServicer):

    def GetProductMetadata(self, request, context):
        try:
            cluster_connection_string = get_cluster_connection_string(request.category)
            client = MongoClient(cluster_connection_string)
            db = client['amazon_metadata']
            collection = db['metadata']
            
            # Construct query based on request
            query = {}
            if request.brand:
                query['brand'] = request.brand
            if request.minPrice:
                query['price'] = {'$gte': request.minPrice}
            if request.maxPrice:
                query['price'] = {'$lte': request.maxPrice}

            documents = collection.find(query)

            # Convert MongoDB documents to gRPC messages
            response = market_performance_pb2.GetProductMetadataResponse()
            for doc in documents:
                product = market_performance_pb2.Product(
                    title=doc.get('title', ''),
                    brand=doc.get('brand', ''),
                    price=doc.get('price', 0.0),
                    rank=doc.get('rank', ''),
                    categories=doc.get('categories', [])
                )
                response.products.append(product)

            return response

        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
    def GetMainCategories(self, request, context):
        main_categories = set()  # Use a set to avoid duplicates
        for cluster in clusters.values():
            client = MongoClient(cluster)
            db = client['amazon_metadata']
            collection = db['metadata']
            categories = collection.distinct("main_cat")  # Assuming "main_cat" is the field name for main categories
            main_categories.update(categories)
        return market_performance_pb2.GetMainCategoriesResponse(mainCategories=list(main_categories))

    def GetTopProducts(self, request, context):
        try:
            cluster_connection_string = get_cluster_connection_string(request.category)
            client = MongoClient(cluster_connection_string)
            db = client['amazon_metadata']
            collection = db['metadata']
            # Adjust the sorting and limit as per your data structure and requirement
            top_products = collection.find({"main_cat": request.category}).sort("rank", 1).limit(2)
            response = market_performance_pb2.GetTopProductsResponse()
            for doc in top_products:
                product = market_performance_pb2.Product(
                    title=doc.get('title', ''),
                    brand=doc.get('brand', ''),
                    price=float(doc.get('price', 0.0)),
                    rank=doc.get('rank', ''),
                    categories=doc.get('categories', [])
                )
                response.topProducts.append(product)
            return response
        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def GetTopBrand(self, request, context):
        try:
            cluster_connection_string = get_cluster_connection_string(request.category)
            client = MongoClient(cluster_connection_string)
            db = client['amazon_metadata']
            collection = db['metadata']
            # MongoDB aggregation to find the brand with the most products
            top_brand = collection.aggregate([
                {"$match": {"main_cat": request.category}},
                {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1}
            ])
            top_brand_list = list(top_brand)
            if top_brand_list:
                return market_performance_pb2.GetTopBrandResponse(
                    topBrand=top_brand_list[0]['_id'], count=top_brand_list[0]['count'])
            return market_performance_pb2.GetTopBrandResponse(topBrand="", count=0)
        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_performance_pb2_grpc.add_MarketPerformanceServiceServicer_to_server(
        MarketPerformanceService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at [::]:50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
