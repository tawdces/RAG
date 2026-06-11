from embedding_service import get_embedding
from vector_db import search_similar

def main():
    while True:
        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        q_vector = get_embedding(question)

        results = search_similar(q_vector, top_k=3)

        print("\n📌 Context :\n")

        for i, r in enumerate(results):
            print(f"\n--- Chunk {i+1} (score: {r['score']:.4f}) ---")
            print(f"File : {r['file_name']}")
            print(f"Page : {r['page']}")
            print()
            print(r["text"])

if __name__ == "__main__":
    main()