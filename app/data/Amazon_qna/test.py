from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#local mongodb connection
#url1 = 'mogodb://127.0.0.1:27017/single_qna'
#mongodb atlas connection
uri = "mongodb+srv://exampleuser:a2lMTHV3KmzBaGM@singleqna.me1c1ax.mongodb.net/"
uri = "mongodb+srv://aylastehling:vdVlFNYHEhmAL3fa@singleqna.me1c1ax.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
#client = MongoClient(url)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)