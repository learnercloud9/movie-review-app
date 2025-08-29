import logging
import azure.functions as func
from pymongo import MongoClient
import os
import json

# MongoDB connection string (set in Azure as Application Setting)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["movieDB"]
collection = db["reviews"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request for reviews API...')

    if req.method == "POST":
        try:
            body = req.get_json()
            movie = body.get("movie")
            rating = body.get("rating")
            comment = body.get("comment")

            if not movie or not rating:
                return func.HttpResponse("Missing movie or rating", status_code=400)

            doc = {"movie": movie, "rating": rating, "comment": comment}
            collection.insert_one(doc)

            return func.HttpResponse(
                json.dumps({"message": "Review added!"}),
                status_code=200,
                mimetype="application/json"
            )
        except Exception as e:
            return func.HttpResponse(str(e), status_code=500)

    elif req.method == "GET":
        reviews = list(collection.find({}, {"_id": 0}))
        return func.HttpResponse(
            json.dumps(reviews),
            status_code=200,
            mimetype="application/json"
        )

    return func.HttpResponse("Method not allowed", status_code=405)
