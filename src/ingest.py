from pathlib import Path
from typing import List
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from mongo import collection
from embedder import get_embedding

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def get_pdf_directory() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "pdf"

def find_pdf_files(pdf_dir: Path) -> List[Path]:
    return sorted(pdf_dir.glob("*.pdf")) + sorted(pdf_dir.glob("*.PDF"))

def build_documents(source: str, page_num: int, chunks: List[str]) -> List[dict]:
    embeddings = [get_embedding(chunk) for chunk in chunks]
    return [
        {
            "source": source,
            "page": page_num,
            "chunk_id": i,
            "text": chunk,
            "embedding": emb,
        }
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]

def ingest_pdf(pdf_path: Path, splitter: RecursiveCharacterTextSplitter) -> int:
    reader = PdfReader(pdf_path)
    inserted = 0

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        chunks = splitter.split_text(text)
        docs = build_documents(pdf_path.name, page_num, chunks)

        if docs:
            collection.insert_many(docs)
            inserted += len(docs)

    return inserted


def ingest_pdf_directory(pdf_dir: Path, splitter: RecursiveCharacterTextSplitter) -> int:
    total = 0
    pdf_files = find_pdf_files(pdf_dir)

    if not pdf_files:
        print("No PDF files found")
        return 0

    for pdf in pdf_files:
        total += ingest_pdf(pdf, splitter)

    return total


def main():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    pdf_dir = get_pdf_directory()
    total = ingest_pdf_directory(pdf_dir, splitter)

    print(f"Done inserting chunks: {total}")


if __name__ == "__main__":
    main()
