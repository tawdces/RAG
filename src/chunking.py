from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str):
    lines = text.split("\n")

    chunks = []
    current = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        candidate = current + "\n" + line if current else line

        if len(candidate) > CHUNK_SIZE:
            if current:
                chunks.append(current.strip())
            current = line
        else:
            current = candidate

    if current:
        chunks.append(current.strip())

    return chunks

def create_chunks(pages):
    all_chunks = []
    chunk_id = 0

    for page in pages:
        page_chunks = chunk_text(page["text"])

        for text in page_chunks:
            all_chunks.append({
                "page": page["page"],
                "chunk_id": chunk_id,
                "text": text
            })
            chunk_id += 1

    return all_chunks