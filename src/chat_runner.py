from embedding_service import get_embedding
from vector_db import search_similar, get_chunk_context

def select_top_chunks(results, threshold):

    if not results:
        return []

    best_score = results[0]["score"]
    selected = []

    for r in results:
        if r["score"] >= best_score - threshold:
            selected.append(r)

    return selected

def deduplicate_chunks(chunks):
    unique = {}

    for c in chunks:
        key = (c["file_name"], c["chunk_id"])
        if key not in unique:
            unique[key] = c

    return list(unique.values())


def build_llm_context(chunks):
    chunks = sorted(chunks, key=lambda x: (x["page"], x["chunk_id"]))

    context = ""
    current_page = None

    for c in chunks:
        text = c["text"].strip()

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

        selected_chunks = select_top_chunks(results, 0.05)

        print("\n==============================")
        print("🔥 SELECTED CHUNKS")
        print("==============================")

        for s in selected_chunks:
            print(f"- chunk {s['chunk_id']} | score={s['score']:.4f}")

        all_expanded = []

        for r in selected_chunks:

            expanded = get_chunk_context(
                r["file_name"],
                r["chunk_id"]
            )

            all_expanded.extend(expanded)

        expanded_chunks = deduplicate_chunks(all_expanded)

        llm_context = build_llm_context(expanded_chunks)

        print("\n==============================")
        print("📌 FINAL LLM CONTEXT")
        print("==============================\n")

        print(llm_context)


if __name__ == "__main__":
    main()