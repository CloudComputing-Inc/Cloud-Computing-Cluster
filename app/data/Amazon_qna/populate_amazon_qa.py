from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
user = "need_user"
password = "needpassword"
up = user + ":" + password

#client = MongoClient("mongodb+srv://"+up+"@single_qna.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient("mongodb://need_user:needpassword@single_qna.mongodb.net:2500/?retryWrites=true&w=majority")
db = client["database"]

# drop everything in there
db.drop_collection("qna")

# open file to parse it
import csv

insert_list = []
with open("app/data/Amazon_qna/single_qna.csv","r",encoding="utf8") as f:
    reader = csv.reader(f)

    first_elem = True
    for row in reader:
        asin = row[1].split("|")
        asin = [ a.strip() for a in asin ]

        if first_elem:
            first_elem = False
            continue

        qna = {
            'asin' : asin,
            'questionType' : row[0].strip(),
            'answerTime' : row[2].strip(),
            'unixTime' : row[3].strip(),
            'question' : row[4].strip(),
            'answerTypre' : row[5].strip(),
            'answer' : row[6].strip()

        }

        # append 
        insert_list.append(qna)

        # insert
        if len(insert_list) >= 100_000:
            result = db.insert_many(insert_list)
            insert_list = []

# insert rest
if len(insert_list) > 0:
    result = db.insert_many(insert_list)
    insert_list = []

print('Done')