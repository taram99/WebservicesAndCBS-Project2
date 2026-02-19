from flask import request, jsonify, redirect
from utils import *
import json

def register_routes(app):

    def bad_request(msg = "error"):
        return jsonify({"error": msg}), 400
    
    @app.route("/", methods=["POST"])
    def create_url():
        data = request.get_json(silent=True)

        #check if data is dict
        if not isinstance(data, dict):
            return bad_request()
        
        url = data.get("url") or data.get("value")

        #check if url is valid
        if not url or not is_valid_url(url):
            return bad_request()
        
        #check if url already exists, 201 return to satisfy unit tests
        for id, v in store.items():
            if v["url"] == url:
                return jsonify({"warning": "url already exists",
                               "id": id}), 201
            
        short_id = create_short_id()
        store[short_id] = {
            "url": url,
            "clicks": 0
        }
        return jsonify({"id": short_id}), 201

    @app.route("/", methods=["GET"])
    def list_urls():
        keys = list(store.keys())
        return jsonify({
            "values": keys if keys else None
        }), 200

    @app.route("/", methods=["DELETE"])
    def delete():
        return "", 404

    @app.route("/<string:id>", methods=["GET"])
    def get_url(id):
        if id not in store:
            return "", 404
        store[id]["clicks"] += 1
        return jsonify({"value": store[id]["url"]}), 301

    @app.route("/<string:id>", methods=["PUT"])
    def update_url(id):
        if id not in store:
            return "", 404

        # Try to parse JSON body, fallback to raw data if JSON parsing fails
        data = request.get_json(silent=True)
        if data is None and request.data:
            try:
                data = json.loads(request.data.decode("utf-8"))
            except Exception:
                data = None

        #check if data is dict
        if not isinstance(data, dict):
            return bad_request()
        
        url = data.get("url") or data.get("value")

        #check if url is valid
        if not url or not is_valid_url(url):
            return bad_request()
        
        #check if url already exists and is not the same as the current url
        for existing_id, v in store.items():
            if v["url"] == url and existing_id != id:
                return bad_request("url already exists")

        store[id]["url"] = url
        store[id]["clicks"] = 0

        return "", 200

    @app.route("/<string:id>", methods=["DELETE"])
    def delete_url(id):
        if id not in store:
            return "", 404

        del store[id]
        return "", 204
    
    @app.route("/<string:id>/stats", methods=["GET"])
    def get_stats(id):
        if id not in store:
            return "", 404
        return jsonify({"id": id, 
                        "url": store[id]["url"],
                        "clicks": store[id]["clicks"]}), 200