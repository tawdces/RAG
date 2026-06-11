import os
from pdf_loader import load_pdf
from text_chunker import create_chunks
from config import PDF_PATH

def main():
    pdf_files = [
        f for f in os.listdir(PDF_PATH)
        if f.endswith(".PDF")
    ]

    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_PATH, pdf_file)

        print(f"\nProcessing: {pdf_file}")

        pages = load_pdf(pdf_path)
        chunks = create_chunks(pages)

        print("Total chunks: ", len(chunks))

if __name__ == "__main__":
    main()