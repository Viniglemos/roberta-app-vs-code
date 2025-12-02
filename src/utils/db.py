import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGODB_URI","mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGODB_DB","roberta_app-db")
MONGO_URL = f"{MONGO_URI}/{MONGO_DB_NAME}"

client = MongoClient(MONGO_URL)
db = client["roberta_app-db"]
clients_collection = db["clients"]
albums_collection = db["albums"]
photos_collection = db["photos"]