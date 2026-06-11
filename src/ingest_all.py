import os
import time
from pdf_loader import load_pdf
from text_chunker import create_chunks
from embedding_service import get_embedding
from vector_db import insert_documents
from config import PDF_PATH
import hashlib

def hash_text(t):
    return hashlib.md5(t.encode()).hexdigest()

def main():

    pdf_files = [
        f for f in os.listdir(PDF_PATH)
        if f.endswith(".PDF")
    ]

    print(f"Found {len(pdf_files)} PDF files")

    success = 0

    seen = set()
    # Deduplicate ทำเฉพาะใน Ram

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_PATH, pdf_file)

        print(f"\nProcessing: {pdf_file}")

        pages = load_pdf(pdf_path)
        chunks = create_chunks(pages)

        print("Total chunks: ", len(chunks))

        for i, c in enumerate(chunks):
            text = c["text"].strip()

            if not text:
                continue

            if text in seen:
                print(f"Skip duplicate chunk {i+1}")
                continue

            try:
                vector = get_embedding(text)

                doc = {
                    "file_name": pdf_file,
                    "page": c["page"],
                    "chunk_id": c["chunk_id"],
                    "text": text,
                    "embedding": vector
                }

                insert_documents([doc])

                seen.add(text)

                success += 1
                print(f"Inserted {i+1}/{len(chunks)}")

            except Exception as e:
                print(f"Error at chunk {i+1}: {e}")

            time.sleep(20)
            # limit 3 request per minute (free tier)

    print("\nDone!")
    print("Total inserted:", success)

if __name__ == "__main__":
    main()