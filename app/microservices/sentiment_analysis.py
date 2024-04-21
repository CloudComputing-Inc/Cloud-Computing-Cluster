from concurrent import futures
import grpc
import reviews_pb2
import reviews_pb2_grpc
from google.cloud import bigquery

project_id = 'bold-sorter-377919'
dataset = 'amazon_reviews'
table = 'electronics'
table_id = f"{project_id}.{dataset}.{table}"  # Update with your BigQuery table ID

class ReviewService(reviews_pb2_grpc.ReviewServiceServicer):
    def __init__(self):
        self.client = bigquery.Client()

    def CreateReview(self, request, context):
        row = {
            "rating": request.rating,
            "title": request.title,
            "text": request.text,
            "images": request.images,
            "asin": request.asin,
            "parent_asin": request.parent_asin,
            "user_id": request.user_id,
            "timestamp": request.timestamp,
            "verified_purchase": request.verified_purchase,
            "helpful_vote": request.helpful_vote
        }
        try:
            errors = self.client.insert_rows_json(table_id, [row])
            if errors:
                raise Exception(errors)
            return reviews_pb2.Review(**request.__dict__)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error creating review: {e}")
            return reviews_pb2.Review()

    def ReadReviewByASIN(self, request, context):
        query = f"SELECT * FROM `{table_id}` WHERE id = {request.asin}"
        try:
            query_job = self.client.query(query)
            rows = query_job.result()
            for row in rows:
                return reviews_pb2.Review(**row)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Review not found")
            return reviews_pb2.Review()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error reading review: {e}")
            return reviews_pb2.Review()

    def UpdateReviewByASIN(self, request, context):
        query = f"""
            UPDATE `{table_id}`
            SET rating={request.rating}, title='{request.title}', text='{request.text}', images='{request.images}',
                asin='{request.asin}', parent_asin='{request.parent_asin}', user_id='{request.user_id}',
                timestamp={request.timestamp}, verified_purchase={request.verified_purchase}, helpful_vote={request.helpful_vote}
            WHERE id = {request.asin}
        """
        try:
            query_job = self.client.query(query)
            query_job.result()
            return reviews_pb2.Review(**request.__dict__)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error updating review: {e}")
            return reviews_pb2.Review()

    def DeleteReviewByASIN(self, request, context):
        query = f"DELETE FROM `{table_id}` WHERE id = {request.asin}"
        try:
            query_job = self.client.query(query)
            query_job.result()
            return reviews_pb2.Review(id=request.id)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error deleting review: {e}")
            return reviews_pb2.Review()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reviews_pb2_grpc.add_ReviewServiceServicer_to_server(ReviewService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
