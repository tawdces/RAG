# อ่านก่อนนนนนนนนนนนนนนนนนนนนนนนน!!!!!!!!!!!!!!!!!!!!!!!!
# เตือนสติตัวเอง ห้ามรัน ingest_test.py มั่วๆโดยไม่อ่าน code ก่อน
# เพราะมี clear_collection() ถ้ารันแล้วข้อมูลจะหายหมด
# กรุณาใส่ # ปิดไว้ดีๆก่อนรัน

import os
import time
from load_pdf import load_pdf
from chunking import create_chunks
from embedding import get_embedding
from database import insert_documents, clear_collection
from config import PDF_PATH
import hashlib

def hash_text(t):
    return hashlib.md5(t.encode()).hexdigest()

def main():
    # TARGET_FILE = "tracker.PDF"
    # pdf_path = os.path.join(PDF_PATH, TARGET_FILE)

    # print(f"\nProcessing: {TARGET_FILE}")

    # pages = load_pdf(pdf_path)
    # chunks = create_chunks(pages)

    # print("Total chunks:", len(chunks))

    # clear_collection() # มี clear_collection() ตรงนี้นะจ้ะ

    # success = 0

    # seen = set()

    # for i, c in enumerate(chunks):
    #     text = c["text"].strip()
    #     if not text:
    #         continue

    #     if hash_text(text) in seen:
    #         print(f"Skip duplicate chunk {i+1}")
    #         continue

    #     try:
    #         vector = get_embedding(text)

    #         doc = {
    #             "file_name": TARGET_FILE,
    #             "page": c["page"],
    #             "chunk_id": c["chunk_id"],
    #             "text": text,
    #             "embedding": vector
    #         }

    #         insert_documents([doc])

    #         seen.add(text)

    #         success += 1
    #         print(f"Inserted {i+1}/{len(chunks)}")

    #     except Exception as e:
    #         print(f"Error at chunk {i+1}: {e}")

    #     time.sleep(20)

    # print("\nDone!")
    # print("Total inserted:", success)

    pdf_files = [
        f for f in os.listdir(PDF_PATH)
        if f.endswith(".PDF")
    ]

    print(f"Found {len(pdf_files)} PDF files")

    # for pdf_file in pdf_files:
    #     pdf_path = os.path.join(PDF_PATH, pdf_file)

    #     print(f"\nProcessing: {pdf_file}")

    #     pages = load_pdf(pdf_path)
    #     chunks = create_chunks(pages)

    #     print("Total chunks: ", len(chunks))

    clear_collection() # มี clear_collection ตรงนี้นะจ้ะ
    # Problem
    # file ใหม่ที่อัพมาเป็น file เดิมที่มีอยู่เเล้ว
    # หาก clear_collection จะทำให้ข้อมูลเก่าหายไปดวย

    success = 0

    seen = set()
    # Problem
    # deduplicate ทำเฉพาะใน Ram

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