from flask import jsonify, request
import grpc
import reviews_pb2
import reviews_pb2_grpc
import connexion

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('reviews.yaml')

# Address and port where the gRPC server is running
GRPC_SERVER_ADDRESS = 'localhost'
GRPC_SERVER_PORT = 50051

def get_reviews():
    # Connect to the gRPC server
    channel = grpc.insecure_channel(f"{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}")
    stub = reviews_pb2_grpc.ReviewServiceStub(channel)
    
    # Make gRPC call to retrieve all reviews
    response = stub.GetReviews(reviews_pb2.Empty())
    
    # Convert gRPC response to JSON
    reviews = [{'id': review.id, 'rating': review.rating, 'title': review.title, 'text': review.text, 'images': review.images, 
                'asin': review.asin, 'parent_asin': review.parent_asin, 'user_id': review.user_id, 'timestamp': review.timestamp, 
                'verified_purchase': review.verified_purchase, 'helpful_vote': review.helpful_vote} for review in response.reviews]
    
    return jsonify(reviews)

@app.route('/reviews', methods=['GET'])
def get_reviews():
    return get_reviews()

@app.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    # Connect to the gRPC server
    channel = grpc.insecure_channel(f"{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}")
    stub = reviews_pb2_grpc.ReviewServiceStub(channel)
    
    # Make gRPC call to retrieve a specific review by ID
    response = stub.GetReviewById(reviews_pb2.ReviewId(id=review_id))
    
    # Convert gRPC response to JSON
    review = {'id': response.id, 'rating': response.rating, 'title': response.title, 'text': response.text, 'images': response.images, 
              'asin': response.asin, 'parent_asin': response.parent_asin, 'user_id': response.user_id, 'timestamp': response.timestamp, 
              'verified_purchase': response.verified_purchase, 'helpful_vote': response.helpful_vote}
    
    return jsonify(review)

@app.route('/reviews', methods=['POST'])
def create_review():
    # Get review data from request
    data = request.json
    
    # Connect to the gRPC server
    channel = grpc.insecure_channel(f"{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}")
    stub = reviews_pb2_grpc.ReviewServiceStub(channel)
    
    # Create a new review using gRPC call
    response = stub.CreateReview(reviews_pb2.Review(**data))
    
    return jsonify({'message': 'Review created successfully', 'id': response.id}), 201

@app.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    # Get review data from request
    data = request.json
    
    # Connect to the gRPC server
    channel = grpc.insecure_channel(f"{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}")
    stub = reviews_pb2_grpc.ReviewServiceStub(channel)
    
    # Update an existing review using gRPC call
    response = stub.UpdateReview(reviews_pb2.UpdateReviewRequest(id=review_id, **data))
    
    return jsonify({'message': 'Review updated successfully'}), 200

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    # Connect to the gRPC server
    channel = grpc.insecure_channel(f"{GRPC_SERVER_ADDRESS}:{GRPC_SERVER_PORT}")
    stub = reviews_pb2_grpc.ReviewServiceStub(channel)
    
    # Delete a review using gRPC call
    response = stub.DeleteReview(reviews_pb2.ReviewId(id=review_id))
    
    return jsonify({'message': 'Review deleted successfully'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
