from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, chunk_size = CHUNK_SIZE, overlap = CHUNK_OVERLAP):
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk
        })

        chunk_id += 1
        start = end - overlap

    return chunks

def create_chunks(pages):
    all_chunks = []

    for page in pages:
        page_text = page["text"]

        page_chunks = chunk_text(page_text)

        for c in page_chunks:
            all_chunks.append({
                "page": page["page"],
                "chunk_id": c["chunk_id"],
                "text": c["text"]
            })

    return all_chunks