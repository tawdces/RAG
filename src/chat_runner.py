from embedding_service import get_embedding
from vector_db import search_similar, rerank_chunks, get_chunk_context

def deduplicate_chunks(chunks):
    unique_chunks = {}

    for chunk in chunks:
        key = (chunk["file_name"], chunk["page"], chunk["chunk_id"])

        if key not in unique_chunks:
            unique_chunks[key] = chunk

    return list(unique_chunks.values())

def build_llm_context(chunks):
    chunks = sorted(chunks, key=lambda item: (item["page"], item["chunk_id"]))

    lines = []
    current_page = None

    for chunk in chunks:
        text = chunk["text"].strip()

        if not text:
            continue

        if current_page != chunk["page"]:
            current_page = chunk["page"]
            lines.extend([f"[Page {current_page}]", ""])

        lines.extend([text, ""])

    return "\n".join(lines).strip()

def run_pipeline(question):

    print("\n==============================")
    print("QUESTION:", question)
    print("==============================\n")

    q_vector = get_embedding(question)

    results = search_similar(q_vector, top_k=10)

    print("\n📌 VECTOR RESULTS")

    for r in results:

        preview = r["text"][:80].replace("\n", " ")

        print(
            f'{r["file_name"]} | '
            f'chunk {r["chunk_id"]} | '
            f'page {r["page"]} | '
            f'score={r["score"]:.4f}\n'
            f'  {preview}...\n'
        )

    reranked = rerank_chunks(question, results)
    selected = reranked[:5]

    print("\n🔥 RERANKED TOP")

    for s in selected:

        print(
            f'{s["file_name"]} | '
            f'chunk {s["chunk_id"]} | '
            f'page {s["page"]} | '
            f'rerank={s["rerank_score"]:.4f}'
        )

    expanded = []

    if selected:
        best_score = selected[0]["rerank_score"]

        for chunk in selected:

            threshold = 0.05

            score_gap = best_score - chunk["rerank_score"]

            if score_gap > threshold:
                continue

            expanded.extend(get_chunk_context(chunk["file_name"], chunk["chunk_id"]))

    expanded = deduplicate_chunks(expanded)

    print("\n🧹 After dedup:", len(expanded))

    return build_llm_context(expanded)

def main():

    while True:
        q = input("\nQuestion: ")

        if q.lower() == "exit":
            break

        context = run_pipeline(q)

        print("\n==============================")
        print("📌 FINAL LLM CONTEXT")
        print("==============================\n")
        print(context)


if __name__ == "__main__":
    main()