import UserExist as e
from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://db:27017")
db = client.MyDb
users = db["Users"]



def Verify_pw(username, password):
    if not e.UserExist(username):
        return False
    hashed_pw = users.find_one({"username": username})["password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False