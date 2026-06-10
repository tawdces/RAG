# RAG Chatbot

Overview

This is a short demo of a Retrieval-Augmented Generation (RAG) chatbot. The
project ingests PDF files, converts them into searchable vectors, and stores
those vectors in MongoDB so the system can find relevant context for questions.

RAG Concept

RAG stands for Retrieval-Augmented Generation. In simple terms:
- The system first retrieves relevant pieces of text (context) from a
	document store using semantic search.
- An LLM (not yet integrated here) would then use that retrieved context to
	generate an answer. Retrieval helps the LLM give more accurate, up-to-date,
	or longer answers without memorizing everything.

Architecture

- `load_pdf.py`: reads PDFs.
- `chunking.py`: splits text into smaller chunks.
- `embedding.py`: creates embeddings using the MongoDB Model API (Voyage).
- `database.py`: stores and queries vectors in MongoDB (uses `pymongo`).
- `ingest_test.py`: example pipeline that ingests PDFs and writes vectors.
- `chat_test.py`: example retrieval that finds similar documents for a query.

Current Status

- The system ingests PDFs, creates embeddings, and stores them in MongoDB.
- It uses MongoDB Vector Search to retrieve semantically similar chunks.
- IMPORTANT: The project currently only retrieves relevant context from
	MongoDB. It does NOT yet call an LLM to generate answers — the output is
	the raw retrieved context.

Tech Stack

- Python
- MongoDB Atlas as the vector database storage
- MongoDB Vector Search for semantic retrieval
- MongoDB Model API key (Voyage embeddings) for generating embeddings
- `pymongo`, `pypdf`, `python-dotenv`, `openai` (see `REQUIREMENTS.txt`)

Files of interest

- [src/ingest_test.py](src/ingest_test.py)
- [src/chat_test.py](src/chat_test.py)
- [src/config.py](src/config.py)