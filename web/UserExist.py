from pymongo import MongoClient

client = MongoClient("mongodb://db:27017")
db = client.MyDb
users = db["Users"]


def UserExist(username):
    user = users.find_one({"username": username})
    if user == None:
        return False
    return True