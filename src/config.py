from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, os.getenv("PDF_FOLDER"))
PDF_FILE = os.getenv("PDF_FILE")
PDF_PATH = os.path.join(PDF_FOLDER, PDF_FILE)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_URI = os.getenv("MONGO_URI")
MONGODB_MODEL_API_KEY = os.getenv("MONGODB_MODEL_API_KEY")