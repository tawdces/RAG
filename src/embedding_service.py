from openai import OpenAI
from config import MONGODB_MODEL_API_KEY, EMBEDDING_MODEL

client = OpenAI(
    api_key = MONGODB_MODEL_API_KEY,
    base_url = "https://ai.mongodb.com/v1"
)

def get_embedding(text: str):
    response = client.embeddings.create(
        model = EMBEDDING_MODEL,
        input = text
    )

    return response.data[0].embedding