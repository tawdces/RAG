import os
from config import PDF_PATH
from pdf_loader import load_pdf
from text_chunker import create_chunks
from embedding_service import get_embedding
from vector_db import insert_documents
import time

def main():
    TARGET_FILE = "....PDF"
    pdf_path = os.path.join(PDF_PATH, TARGET_FILE)

    print(f"\nProcessing: {TARGET_FILE}")

    pages = load_pdf(pdf_path)
    chunks = create_chunks(pages)

    print("Total chunks:", len(chunks))

    success = 0

    seen = set()

    for i, c in enumerate(chunks):
        text = c["text"].strip()

        if not text:
            continue

        key = (TARGET_FILE, c["page"], c["chunk_id"])

        if key in seen:
            continue

        try:
            vector = get_embedding(text)

            doc = {
                "file_name": TARGET_FILE,
                "page": c["page"],
                "chunk_id": c["chunk_id"],
                "text": text,
                "embedding": vector
            }

            insert_documents([doc])

            seen.add(key)

            success += 1
            print(f"Inserted {i+1}/{len(chunks)}")

        except Exception as e:
            print(f"Error at chunk {i+1}: {e}")

        time.sleep(20)

    print("\nDone!")
    print("Total inserted:", success)

if __name__ == "__main__":
    main()