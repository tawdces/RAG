from embedding_service import get_embedding
from vector_db import search_similar, get_chunk_context

def build_llm_context(expanded_chunks):
    expanded_chunks = sorted(
        expanded_chunks,
        key=lambda x: (x["page"], x["chunk_id"])
    )

    context = ""
    current_page = None
    seen_text = set()

    for c in expanded_chunks:

        if current_page != c["page"]:
            current_page = c["page"]
            context += f"\n[Page {current_page}]\n\n"

        if c["text"] in seen_text:
            continue

        seen_text.add(c["text"])

        context += c["text"].strip() + "\n\n"

    return context

def main():
    while True:
        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        q_vector = get_embedding(question)

        results = search_similar(q_vector, top_k=3)

        print("\n==============================")
        print("📌 ORIGINAL VECTOR SEARCH RESULT")
        print("==============================\n")

        expanded_contexts = []

        for i, r in enumerate(results):

            print(f"\n--- TOP {i+1} ---")
            print(f"File : {r['file_name']}")
            print(f"Chunk ID : {r['chunk_id']}")
            print(f"Score : {r['score']:.4f}")
            print(r["text"])

            expanded = get_chunk_context(r["file_name"], r["chunk_id"])

            expanded_contexts.append({
                "original": r,
                "expanded": expanded
            })

        print("\n==============================")
        print("📌 FINAL LLM CONTEXT BLOCKS")
        print("==============================\n")

        llm_blocks = []

        for i, item in enumerate(expanded_contexts):

            llm_context = build_llm_context(item["expanded"])

            block = {
                "block_id": i + 1,
                "file": item["original"]["file_name"],
                "score": item["original"]["score"],
                "chunk_id": item["original"]["chunk_id"],
                "context": llm_context
            }

            llm_blocks.append(block)

            print(f"\n\n######## BLOCK {block['block_id']} ########")
            print(f"File: {block['file']}")
            print(f"Original Chunk ID: {block['chunk_id']}")
            print(f"Score: {block['score']:.4f}")

            print("\n--- CONTEXT (FOR LLM) ---")
            print(block["context"])
            print("-" * 60)

if __name__ == "__main__":
    main()