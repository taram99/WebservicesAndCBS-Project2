from flask import Flask
from routes2 import auth_routes

app = Flask(__name__)

app.register_blueprint(auth_routes)

def home():
    return "Auth service running"


if __name__ == "__main__":
    app.run(port=8001, debug=True)