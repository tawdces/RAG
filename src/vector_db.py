from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, MONGODB_MODEL_API_KEY, RERANKING_MODEL
from voyageai import Client

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

voyage_client = Client(MONGODB_MODEL_API_KEY)

def insert_documents(docs):

    if docs:
        collection.insert_many(docs)

def clear_collection():
    collection.delete_many({})

def search_similar(vector, top_k=10):
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": vector,
                "numCandidates": top_k * 10,
                "limit": top_k
            }
        },
        {
            "$project": {
                "_id": 0,
                "file_name": 1,
                "page": 1,
                "chunk_id": 1,
                "text": 1,
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

def rerank_chunks(query, chunks):
    
    if not chunks:
        return []

    documents = [c["text"] for c in chunks]

    response = voyage_client.rerank(
        model = RERANKING_MODEL,
        query = query,
        documents = documents
    )

    reranked = []

    for r in response.results:
        idx = r.index
        score = r.relevance_score

        item = chunks[idx]
        item["rerank_score"] = score
        reranked.append(item)

    return reranked