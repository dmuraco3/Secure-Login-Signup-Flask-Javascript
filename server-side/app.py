import flask
from flask import request, jsonify, make_response
from flask_cors import CORS
import json
import hashlib

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/login/', methods=['POST'])
def login():
    username = request.json.get('username')
    Hash = request.json.get('Hash')
    print(username, " : ", Hash)

    with open("server-side/usernames.json") as file:
        data = json.load(file)
        length = len(data)
        for v in data:
            if username == data[v]["username"]:
                username_exists = True
                break
            else:
                if data[v] == data[str(length)]:
                    return jsonify(success=False), 418

    if username_exists:
        print("that username exists")
        with open("server-side/SensitiveInfo.json") as file2:
            Info = json.load(file2)
            for x in Info:
                if str(username) == Info[x]["username"]:
                    if Hash == Info[x]["hash"]:
                        print("that password is correct")
                        return (jsonify(success=True), 201)
                    else:
                        print("that password is incorrect")
                        return (jsonify(success=False), 400)

def write_username(data, filename='server-side/usernames.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def write_hash(data, filename='server-side/sensitiveInfo.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def generate_hash(filename='server-side/sensitiveInfo.json'):
    with open(filename) as f:
        json.load(f)

@app.route('/signup/', methods=['post']) # api endpoint for signup
def signup(filename="server-side/sensitiveInfo.json"):
    username = request.json.get('username')
    email = request.json.get('email')
    Hash = request.json.get('Hash')
    print(username, " : ", email, " : ", Hash)

    with open(filename) as file:
        data = json.load(file)
        length = len(data)
        for v in data:
            if email == data[v]["email"]:
                print("that email has already been used")
                return jsonify(success=False), 400
            else:
                if username == data[v]["username"]:
                    print("that username is unavailable")
                    return jsonify(success=False), 418
                else:
                    if data[v] == data[str(length)]:
                        print("that username is available")
                        user_available = True
    
    if user_available:
        with open(filename) as json_file:
            data = json.load(json_file)
            data[str(len(data) + 1)] = {
                "username": str(username)
                }

            print(data)
            write_username(data)
        with open(filename) as json_file:
            data = json.load(json_file)
            data[str(len(data) + 1)] = {
                "username": str(username),
                "email": str(email),
                "hash": str(Hash)
            }
            print(data)
            write_hash(data)


        return jsonify(success=True), 201
        

app.run()