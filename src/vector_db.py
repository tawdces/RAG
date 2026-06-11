from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def insert_documents(docs):
    if docs:
        collection.insert_many(docs)

def clear_collection():
    collection.delete_many({})

def search_similar(vector, top_k=3):
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": vector,
                "numCandidates": 50,
                "limit": top_k
            }
        },
        {
            "$project": {
                "_id": 0,
                "file_name": 1,
                "text": 1,
                "page": 1,
                "chunk_id": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))

def get_chunk_context(file_name, chunk_id):
    return list(collection.find({
        "file_name": file_name,
        "chunk_id": {
            "$in": [chunk_id - 1, chunk_id, chunk_id + 1]
        }
    }, {
        "_id": 0,
        "file_name": 1,
        "page": 1,
        "chunk_id": 1,
        "text": 1
    }).sort("chunk_id", 1))