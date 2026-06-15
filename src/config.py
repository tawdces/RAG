from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_PATH = os.path.join(BASE_DIR, os.getenv("PDF_FOLDER"))

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
RERANKING_MODEL = os.getenv("RERANKING_MODEL")
MONGODB_MODEL_API_KEY = os.getenv("MONGODB_MODEL_API_KEY")

MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")