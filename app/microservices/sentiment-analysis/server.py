from concurrent import futures
import grpc
import reviews_pb2
import reviews_pb2_grpc
import psycopg2

class ReviewService(reviews_pb2_grpc.ReviewServiceServicer):
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='reviews',
            user='chranama',
            password='password',
            host='localhost',
            port='5432'
        )

    def _execute_query(self, query, args=None):
        cursor = self.conn.cursor()
        cursor.execute(query, args)
        self.conn.commit()
        return cursor

    def CreateReview(self, request, context):
        query = """
            INSERT INTO reviews (rating, title, text, images, asin, parent_asin, user_id, timestamp, verified_purchase, helpful_vote)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor = self._execute_query(query, (
            request.rating,
            request.title,
            request.text,
            request.images,
            request.asin,
            request.parent_asin,
            request.user_id,
            request.timestamp,
            request.verified_purchase,
            request.helpful_vote
        ))
        review_id = cursor.fetchone()[0]
        return reviews_pb2.Review(id=review_id, **request.__dict__)

    def ReadReviewById(self, request, context):
        query = "SELECT * FROM reviews WHERE id = %s"
        cursor = self._execute_query(query, (request.id,))
        row = cursor.fetchone()
        if row:
            return reviews_pb2.Review(
                id=row[0],
                rating=row[1],
                title=row[2],
                text=row[3],
                images=row[4],
                asin=row[5],
                parent_asin=row[6],
                user_id=row[7],
                timestamp=row[8],
                verified_purchase=row[9],
                helpful_vote=row[10]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Review not found")
            return reviews_pb2.Review()

    def UpdateReview(self, request, context):
        query = """
            UPDATE reviews
            SET rating=%s, title=%s, text=%s, images=%s, asin=%s, parent_asin=%s, user_id=%s, timestamp=%s, verified_purchase=%s, helpful_vote=%s
            WHERE id = %s
            RETURNING *
        """
        cursor = self._execute_query(query, (
            request.rating,
            request.title,
            request.text,
            request.images,
            request.asin,
            request.parent_asin,
            request.user_id,
            request.timestamp,
            request.verified_purchase,
            request.helpful_vote,
            request.id
        ))
        row = cursor.fetchone()
        if row:
            return reviews_pb2.Review(
                id=row[0],
                rating=row[1],
                title=row[2],
                text=row[3],
                images=row[4],
                asin=row[5],
                parent_asin=row[6],
                user_id=row[7],
                timestamp=row[8],
                verified_purchase=row[9],
                helpful_vote=row[10]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Review not found")
            return reviews_pb2.Review()

    def DeleteReview(self, request, context):
        query = "DELETE FROM reviews WHERE id = %s RETURNING *"
        cursor = self._execute_query(query, (request.id,))
        row = cursor.fetchone()
        if row:
            return reviews_pb2.Review(
                id=row[0],
                rating=row[1],
                title=row[2],
                text=row[3],
                images=row[4],
                asin=row[5],
                parent_asin=row[6],
                user_id=row[7],
                timestamp=row[8],
                verified_purchase=row[9],
                helpful_vote=row[10]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Review not found")
            return reviews_pb2.Review()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reviews_pb2_grpc.add_ReviewServiceServicer_to_server(ReviewService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()