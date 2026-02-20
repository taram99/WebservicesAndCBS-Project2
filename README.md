URL Shortening Service with JWT Authentication

This project implements a microservice-based REST architecture consisting of two independent services:

Authentication Service (port 8001)
Handles user registration, password updates, login, and JSON Web Token (JWT) generation and validation.

URL Shortening Service (port 8000)
Allows authenticated users to create, update, retrieve, and delete shortened URLs. Each shortened URL is associated with its owner.


The system follows a simple microservice design:
Users authenticate via the Authentication Service.
Upon successful login, a signed JWT is issued.
The URL Shortening Service validates this token by communicating with the Authentication Service.
Only authenticated users can create and manage their own shortened URLs.

Security:
JWTs are signed using HMAC-SHA256.
Tokens are validated before any protected operation.
URL ownership is enforced: users can only modify or delete their own URLs.
User credentials are stored in-memory.

How to run:

Requirements
Install the dependencies:
pip install -r requirements.txt

Start both services in seperate terminals:

Url shortener:
python shortening_service/app.py

Authentication service:
python auth_service/app2.py
