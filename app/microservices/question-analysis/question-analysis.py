import grpc
import question_analysis_pb2
import question_analysis_pb2_grcp
from pymongo import MongoClient
from concurrent import futures

# connect to MongoDB, change the user and passwordX  to reflect your own clusters  connection strings
user = "exampleuser"
password = "Ra2lMTHV3KmzBaGM"
up = user + ":" + password

client = MongoClient("mongodb+srv://"+up+"@single_qna.mongodb.net/Qna?retryWrites=true&w=majority")
db = client["database"]
collection = db["qna"]

class LanguageAnalysisService(question_analysis_pb2_grcp.LanguageAnalysisServiceServicer):
    def GetStringAnswer(self, request, context):
        try:
            #Construct query based on request
            query = {}
            if request.asin:
                query['asin'] = request.asin
            if request.question:
                query['question'] = request.question

            documents = collection.find(query)

            # Convert MongoDB documents to gRPC messages
            response = question_analysis_pb2.GetStringAnswerResponse()
            for doc in documents:
                answer = question_analysis_pb2.QAndA(
                    answer = doc.get('answer', ''),
                    product = doc.get('asin', ''),
                )
                response.qAndA.append(answer)
            
            return response
        
        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        

    def GetProductProductAnswer(self, request, context):
        try:
            query = {}
            if request.asin:
                query['asin'] = request.asin

            documents = collection.find(query)

            response = question_analysis_pb2.GetProductAnswerResponse()
            for doc in documents:
                answer = question_analysis_pb2.QAndA(
                    answer = doc.get('answer', '')
                )
                response.qAndA.append(answer)

            return response

        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))
    
    def GetAnswerType(self, request, context):
        try:
            query = {}
            if request.asin:
                query['asin'] = request.asin
            if request.answer:
                query['answer'] = request.answer

            documents = collection.find(query)

            response = question_analysis_pb2.GetProductAnswerResponse()
            for doc in documents:
                answer = question_analysis_pb2.QAndA(
                    answerType = doc.get('answerType', '')
                )
                response.qAndA.append(answer)

            return response

        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def GetQuestionType(self, request, context):
        try:
            query = {}
            if request.asin:
                query['asin'] = request.asin
            if request.question:
                query['question'] = request.question

            documents = collection.find(query)

            response = question_analysis_pb2.GetProductAnswerResponse()
            for doc in documents:
                answer = question_analysis_pb2.QAndA(
                    questionType = doc.get('questionType', '')
                )
                response.qAndA.append(answer)

            return response

        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    def GetTimeOfAnswer(self, request, context):
        try:
            query = {}
            if request.asin:
                query['asin'] = request.asin
            if request.question:
                query['question'] = request.question

            documents = collection.find(query)

            response = question_analysis_pb2.GetProductAnswerResponse()
            for doc in documents:
                answer = question_analysis_pb2.QAndA(
                    answerTome = doc.get('answerTime', '')
                )
                response.qAndA.append(answer)

            return response

        except ValueError as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    question_analysis_pb2_grcp.add_LanguageAnalysisServiceServicer_to_server(
        LanguageAnalysisService(), server
    )
    server.add_insecure_port('[::]:50055')
    server.start()
    print("Server started at [::]:50055")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()