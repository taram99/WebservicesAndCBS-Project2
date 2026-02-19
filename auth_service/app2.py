from flask import Flask

app = Flask(__name__)

def home():
    return "Auth service running"


if __name__ == "__main__":
    app.run(port=5001, debug=True)