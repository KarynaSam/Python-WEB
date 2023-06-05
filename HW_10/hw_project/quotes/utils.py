from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb+srv://Module9:wLcuUrRbu7CK2Y3d@eridas.p3ye6ga.mongodb.net/")

    db = client.hw10
    return db