import os
import time
from load_pdf import load_pdf
from chunking import create_chunks
from embedding import get_embedding
from database import insert_documents, clear_collection
from config import PDF_PATH

def main():
    pdf_files = [
        f for f in os.listdir(PDF_PATH)
        if f.endswith(".PDF")
    ]

    # print(f"Found {len(pdf_files)} PDF files")

    # for pdf_file in pdf_files:
    #     pdf_path = os.path.join(PDF_PATH, pdf_file)

    #     print(f"\nProcessing: {pdf_file}")

    #     pages = load_pdf(pdf_path)
    #     chunks = create_chunks(pages)

    #     print("Total chunks: ", len(chunks))

    # clear_collection()
    # Problem
    # file ใหม่ที่อัพมาเป็น file เดิมที่มีอยู่เเล้ว
    # หาก clear_collection จะทำให้ข้อมูลเก่าหายไปดวย

    success = 0

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_PATH, pdf_file)

        print(f"\nProcessing: {pdf_file}")

        pages = load_pdf(pdf_path)
        chunks = create_chunks(pages)

        print("Total chunks: ", len(chunks))

        for i, c in enumerate(chunks):
            try:
                vector = get_embedding(c["text"])

                doc = {
                    "file_name": pdf_file,
                    "page": c["page"],
                    "chunk_id": c["chunk_id"],
                    "text": c["text"],
                    "embedding": vector
                }

                insert_documents([doc])

                success += 1
                print(f"Inserted {i+1}/{len(chunks)}")
                # Problem
                # embedding -> insert / embedding -> store -> insert

            except Exception as e:
                print(f"Error at chunk {i+1}: {e}")

            time.sleep(20)
            # Problem
            # limit 3 request per minute (free tier)

    print("\nDone!")
    print("Total inserted:", success)

if __name__ == "__main__":
    main()