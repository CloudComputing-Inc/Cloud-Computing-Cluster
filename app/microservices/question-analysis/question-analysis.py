import grpc
import question_analysis_pb2
import question_analysis_pb2_grcp
from pymongo import MongoClient
from concurrent import futures

# connect to MongoDB, change the user and passwordX  to reflect your own clusters  connection strings
user = "need_user"
password = "needpassword"
up = user + ":" + password

client = MongoClient("mongodb+srv://"+up+"@qna.lnpq3.mongodb.net/Qna?retryWrites=true&w=majority")
db = client["database"]
db = db["qna"]

