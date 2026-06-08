import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

load_dotenv()

def get_mongo_uri() -> str:
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise EnvironmentError("MONGO_URI is not set in the environment")
    return uri

def get_mongo_client(uri: str) -> MongoClient:
    return MongoClient(uri)

def get_collection() -> Collection:
    client = get_mongo_client(get_mongo_uri())
    db_name = os.getenv("DB_NAME", "rag_db")
    collection_name = os.getenv("COLLECTION_NAME", "chunks")
    return client[db_name][collection_name]

collection = get_collection()

# if __name__ == "__main__":
#     try:
#         client = get_mongo_client(get_mongo_uri())

#         client.admin.command("ping")

#         print("✅ MongoDB connected successfully")

#         db_name = os.getenv("DB_NAME", "rag_db")
#         collection_name = os.getenv("COLLECTION_NAME", "chunks")

#         print(f"Database: {db_name}")
#         print(f"Collection: {collection_name}")

#     except Exception as e:
#         print("❌ MongoDB connection failed")
#         print(e)

if __name__ == "__main__":
    print("Mongo connected")
