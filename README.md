# RAG Chatbot

Overview

A small Retrieval-Augmented Generation (RAG) demo in Python. The project
ingests PDFs, turns text into vector embeddings, and stores them in MongoDB.
Current stage: ingestion + embedding + vector storage and retrieval (no LLM
integration yet).

Tech stack

- Python
- MongoDB Atlas (vector database)
- MongoDB Vector Search (semantic retrieval)
- Voyage embeddings (`voyage-3-large`) via the MongoDB Model API
- Key Python packages listed in `REQUIREMENTS.txt`

Architecture (high level)

1. PDF Loader → 2. Chunking → 3. Embedding → 4. MongoDB storage

- PDF Loader: reads PDF files and extracts text ([src/pdf_loader.py](src/pdf_loader.py)).
- Chunking: splits text into smaller chunks for embedding ([src/text_chunker.py](src/text_chunker.py)).
- Embedding: calls the Voyage embedding model (`voyage-3-large`) to produce vectors ([src/embedding_service.py](src/embedding_service.py)).
- Storage: writes vectors and metadata to MongoDB and enables vector search ([src/vector_db.py](src/vector_db.py)).
- Ingest scripts: `ingest_file.py` / `ingest_all.py` run the ingestion pipeline.
- Retrieval / test runner: `chat_runner.py` demonstrates querying and returning raw retrieved context.

Project structure

```
README.md
REQUIREMENTS.txt
src/
  pdf_loader.py
  text_chunker.py
  embedding_service.py
  vector_db.py
  ingest_file.py
  ingest_all.py
  chat_runner.py
  config.py
  reset_collection.py
  validate_files.py
data/
  pdf/
```

Current limitation

- The pipeline for ingestion, embedding, and retrieval is implemented.
- The system does NOT yet call an LLM to generate final answers. Retrieved
  results are returned as raw context (no response-generation step).

Setup (basic)

1. Install dependencies:

```bash
pip install -r REQUIREMENTS.txt
```

2. Create a `.env` file with at least:

```text
MONGO_URI=your_mongodb_atlas_uri
MONGO_DB=your_db_name
MONGO_COLLECTION=your_collection
MONGODB_MODEL_API_KEY=your_mongodb_model_api_key
EMBEDDING_MODEL=voyage-3-large
PDF_PATH=data/pdf
```

3. Ingest documents (example):

```bash
python src/ingest_all.py
```

4. Run a retrieval demo:

```bash
python src/chat_runner.py
```

Future work

- Add LLM integration to generate final answers from retrieved context (RAG
  completion stage).
- Improve retrieval ranking and filtering.
- Add an API layer (e.g., FastAPI) for serving queries.

License

Provided as-is for experimentation.
