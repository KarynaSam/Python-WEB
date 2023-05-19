from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Module9:wLcuUrRbu7CK2Y3d@eridas.p3ye6ga.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

db = client.web9

if __name__ == '__main__':

    result_one = db.privat24.find()
    for result in result_one:
        print(result)


