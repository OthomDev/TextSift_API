from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy
import UserExist as e
import verifyPw as v

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.MyDb
users = db["Users"]











def countTokens(username):
    tokens =  users.find_one({"username": username})["Tokens"]
    return tokens



class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]


        if e.UserExist(username):
            retJson= {
                "Status Code":301,
                "msg": "Invalid username"
            }
            return jsonify(retJson)
        
        hashed_pw =  bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "username": username,
            "password": hashed_pw,
            "Tokens": 6

        })

        retJson = {
            "Status code": 200,
            "msg": "You've successfully signed up to the API"
        }
        return jsonify(retJson)




class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not e.UserExist(username):
            retJson= {

                "Status Code":301,
                "msg": "Invalid username"
            }
            return jsonify(retJson)
        
        correct_pw = v.Verify_pw(username, password)

        if not correct_pw:
            retJson = {
                "Status Code": 302,
                "msg": "Invalid Password"
            }
            return jsonify(retJson)

        tokens = countTokens(username)

        if tokens <= 0:
            retJson={
                "Status Code": 303,
                "msg": "Insufficient tokens. Please replenish your balance to continue using our services."
            }
            return jsonify(retJson)
        
        
        nlp = spacy.load("en_core_web_sm")

        text1 = nlp(text1)
        text2 = nlp(text2)

        # Ration is a number  0 and 1, closer to 1, means text1 more similiar to text2 

        ratio = text1.similarity(text2)
        
        
        users.update_one({"username": username}, {"$set": { "Tokens":  tokens-1}})



        retJson={
            "Status Code": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfully"

        }
        return jsonify(retJson)

        

    
        





class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]

        if not e.UserExist(username):
            retJson = {
                "Status Code": 301,
                "msg": "Invalid username"
            }
            return jsonify(retJson)
        correct_admin_pass = "abc123"
        if not password == correct_admin_pass:
            retJson = {
                "Status Code": 304,
                "msg": "Your token balance is low. Please contact our support team to assist with your refill."
            }
            return jsonify(retJson)
        
        current_tokens = countTokens(username)
        users.update_one({"username": username}, {"$set": { "Tokens": current_tokens + refill_amount}})

        retJson = {
            "Status Code": 200,
            "msg": "Refilled successfully! Thank you for topping up your account."
        }
        return jsonify(retJson)




api.add_resource(Register, "/register")
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0')

