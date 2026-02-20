from jwtauth import validating_jwt, generating_jwt
from flask import Blueprint, jsonify, request

auth_routes = Blueprint("auth_routes", __name__)
users = {}

@auth_routes.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return "Duplicate", 409
    
    users[username] = password
    return "", 201
    

@auth_routes.route("/users", methods=["PUT"])
def update_password():
    data = request.get_json()
    username = data.get("username")
    password_old = data.get("old-password")
    password_new = data.get("new-password")

    if username not in users or users[username] != password_old:
        return "forbidden", 403
    
    users[username] = password_new
    return "", 200

@auth_routes.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users or users[username] != password:
        return "forbidden", 403
    
    token = generating_jwt(username)
    return jsonify({"token": token}), 200

@auth_routes.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    token = data.get("token")

    print("Received JSON:", data)

    if not token:
        return "Forbidden", 403
    
    username = validating_jwt(token)

    if not username:
        return "Forbidden", 403
    
    return jsonify({"username": username}), 200

