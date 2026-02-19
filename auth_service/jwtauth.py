import base64
import hmac
import hashlib
import json
import os

#print(os.environ.get("JWT_SECRET"))

SECRET = os.environ.get("JWT_SECRET")

def base64UrlEncode(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")
    

def generating_jwt(username):
    #alg is the signing algorithm
    header = {
    "alg": "HS256",
    "typ": "JWT"
    }
    #now Json is base64 encoded

    payload = {"username": username}



    header_b64 =  base64UrlEncode(header) 
    payload_b64 = base64UrlEncode(payload)

    message = f"{header_b64}.{payload_b64}"

    signature = hmac.new(SECRET.encode(), message.encode(), hashlib.sha256).digest()

    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{message}.{signature_b64}"


#function to make sure username in token cannot be changed
def validating_jwt(token):
    try:
        #split token
        header_b64, payload_b64, signature_b64 = token.split(".")
        #signed message
        message = f"{header_b64}.{payload_b64}"
        #recompute what signature should be
        expected_signature = hmac.new(
            SECRET.encode(), 
            message.encode(), 
            hashlib.sha256
            ).digest()
        #encode it and convert to base64 format
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip("=")
        #compare signatures
        if signature_b64 != expected_signature_b64:
            return None
        #if signature is valid decode payload
        payload_json = base64.urlsafe_b64decode(
            payload_b64 + "=="
            ).decode()
        #extract username out of token
        payload = json.loads(payload_json)

        return payload.get("username")
    

    except Exception:
        return None
    




