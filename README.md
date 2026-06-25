# RAG Chatbot

## Overview

A Retrieval-Augmented Generation (RAG) application in Python that enables semantic search over PDF documents. The system ingests PDFs, converts text into vector embeddings, stores them in MongoDB, and provides multi-stage retrieval with reranking and context expansion.

**Current capabilities:**
- PDF ingestion and text extraction
- Semantic chunking with configurable chunk size
- Vector embeddings via Voyage AI
- MongoDB vector search with semantic similarity
- Reranking of search results
- Interactive query interface

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
- Retrieval / test runner: `chat_runner.py` demonstrates querying, reranking, and returning retrieved context.
- Utility scripts: `reset_collection.py` clears the MongoDB collection; `validate_files.py` checks PDF integrity.

## Environment configuration

Create a `.env` file in the project root with the following variables:

```text
# MongoDB
MONGO_URI=your_mongodb_atlas_uri
MONGO_DB=your_database_name
MONGO_COLLECTION=your_collection_name

# Embeddings
MONGODB_MODEL_API_KEY=your_mongodb_model_api_key
EMBEDDING_MODEL=voyage-3-large
RERANKING_MODEL=your_reranking_model_name

# Files
PDF_FOLDER=data/pdf
CHUNK_SIZE=512
```

**Required variables:**
- `MONGO_URI`: MongoDB Atlas connection string
- `MONGO_DB`: Database name
- `MONGO_COLLECTION`: Collection name for storing vectors
- `MONGODB_MODEL_API_KEY`: API key for Voyage AI embeddings
- `PDF_FOLDER`: Relative path to PDF directory

## Scripts overview

| Script | Purpose |
|--------|---------|
| `ingest_file.py` | Ingest a single PDF file into the vector database |
| `ingest_all.py` | Ingest all PDFs from the configured folder |
| `chat_runner.py` | Interactive query interface with vector search, reranking, and context expansion |
| `reset_collection.py` | Clear all documents from the MongoDB collection |
| `validate_files.py` | Validate PDF files in the data folder |
| `config.py` | Configuration loader (reads from `.env`) |
| `pdf_loader.py` | PDF text extraction utility |
| `text_chunker.py` | Text splitting into chunks |
| `embedding_service.py` | Embedding generation via Voyage AI |
| `vector_db.py` | MongoDB vector search and reranking operations |

## Project structure

```
README.md
REQUIREMENTS.txt
src/
  pdf_loader.py          # Extract text from PDFs
  text_chunker.py        # Split text into chunks
  embedding_service.py   # Generate embeddings
  vector_db.py           # MongoDB operations and reranking
  ingest_file.py         # Single file ingestion
  ingest_all.py          # Batch ingestion
  chat_runner.py         # Interactive retrieval demo
  config.py              # Environment configuration
  reset_collection.py    # Clear MongoDB collection
  validate_files.py      # Validate PDF files
data/
  pdf/                   # PDF storage location
```

## Retrieval pipeline

The `chat_runner.py` script implements a multi-stage retrieval pipeline:

1. **Query embedding**: Convert user question to vector using Voyage AI
2. **Vector search**: Find top 10 similar chunks from MongoDB using vector similarity
3. **Reranking**: Use a reranking model to prioritize most relevant results
4. **Context expansion**: Retrieve surrounding chunks for better context
5. **Deduplication**: Remove duplicate chunks
6. **Context building**: Format results as structured context for LLM integration

## Current status

- ✅ PDF ingestion, chunking, and embedding
- ✅ Vector storage in MongoDB with semantic search
- ✅ Reranking and context expansion
- ❌ LLM integration for response generation (future work)
- ❌ API layer for serving queries (future work)

## Setup

### 1. Install dependencies

```bash
pip install -r REQUIREMENTS.txt
```

Required packages:
- `pymongo` — MongoDB client
- `pypdf` — PDF reading
- `openai` — LLM integration (future use)
- `python-dotenv` — Environment variable management
- Additional: `voyageai` — Voyage AI embeddings (check if in REQUIREMENTS.txt)

### 2. Configure environment

Create a `.env` file in the project root with required variables (see Environment configuration section above).

### 3. Ingest documents

Ingest all PDFs from the configured folder:

```bash
python src/ingest_all.py
```

Or ingest a single file (edit `TARGET_FILE` in the script):

```bash
python src/ingest_file.py
```

### 4. Run retrieval demo

Start an interactive query session:

```bash
python src/chat_runner.py
```

Type your questions and press Enter. Type `exit` to quit.

### Utility commands

Reset the MongoDB collection:

```bash
python src/reset_collection.py
```

Validate PDF files:

```bash
python src/validate_files.py
```

## Future work

**Immediate next steps:**
- LLM integration to generate final answers from retrieved context (RAG completion stage)
- Add API layer (e.g., FastAPI) for serving queries over HTTP

**Potential improvements:**
- Improve retrieval ranking and filtering
- Hybrid search combining dense and sparse retrieval
- Query expansion and multi-turn conversations
- Caching for frequently asked questions
- Evaluation metrics for retrieval quality

License

Provided as-is for experimentation.
