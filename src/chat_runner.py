from embedding_service import get_embedding
from vector_db import search_similar, get_chunk_context
import hashlib

def hash_text(t):
    return hashlib.md5(t.encode()).hexdigest()

def is_low_confidence(results):
    if len(results) < 2:
        return False

    return (results[0]["score"] - results[1]["score"]) < 0.05

def select_top_chunks(results):
    selected = []

    selected.append(results[0])

    if is_low_confidence(results):
        selected.append(results[1])

    return selected

def build_llm_context(expanded_chunks):

    expanded_chunks = sorted(
        expanded_chunks,
        key=lambda x: (x["page"], x["chunk_id"])
    )

    context = ""
    current_page = None

    seen_hashes = set()

    for c in expanded_chunks:

        text = c["text"].strip()
        text_hash = hash_text(text)

        if text_hash in seen_hashes:
            continue

        seen_hashes.add(text_hash)
        
        if current_page != c["page"]:
            current_page = c["page"]
            context += f"\n[Page {current_page}]\n\n"

        context += text + "\n\n"

    return context

def main():
    while True:
        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        q_vector = get_embedding(question)

        results = search_similar(q_vector, top_k=3)

        print("\n==============================")
        print("📌 VECTOR SEARCH RESULTS")
        print("==============================\n")

        for i, r in enumerate(results):
            print(f"\n--- TOP {i+1} ---")
            print(f"File : {r['file_name']}")
            print(f"Chunk ID : {r['chunk_id']}")
            print(f"Score : {r['score']:.4f}")
            print(r["text"])

        selected_chunks = select_top_chunks(results)

        print("\n==============================")
        print("🔥 SELECTED CHUNKS")
        print("==============================")

        for s in selected_chunks:
            print(f"- chunk {s['chunk_id']} | score={s['score']:.4f}")

        expanded_contexts = []

        for r in selected_chunks:

            expanded = get_chunk_context(
                r["file_name"],
                r["chunk_id"]
            )

            expanded_contexts.append({
                "original": r,
                "expanded": expanded
            })

        print("\n==============================")
        print("📌 FINAL LLM CONTEXT")
        print("==============================\n")

        llm_blocks = []

        for i, item in enumerate(expanded_contexts):

            llm_context = build_llm_context(item["expanded"])

            block = {
                "block_id": i + 1,
                "file": item["original"]["file_name"],
                "chunk_id": item["original"]["chunk_id"],
                "score": item["original"]["score"],
                "context": llm_context
            }

            llm_blocks.append(block)

            print(f"\n\n######## BLOCK {block['block_id']} ########")
            print(f"File: {block['file']}")
            print(f"Chunk ID: {block['chunk_id']}")
            print(f"Score: {block['score']:.4f}")

            print("\n--- CONTEXT (FOR LLM) ---")
            print(block["context"])
            print("-" * 60)

if __name__ == "__main__":
    main()