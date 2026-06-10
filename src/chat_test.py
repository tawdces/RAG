from embedding import get_embedding
from database import search_similar

def main():
    while True:
        question = input("\n--- Question: ")

        if question.lower() == "exit":
            break

        q_vector = get_embedding(question)

        results = search_similar(q_vector, top_k=3)

        print("\n📌 Context :\n")

        for i, r in enumerate(results):
            print(f"\n--- Chunk {i+1} (score: {r['score']:.4f}) ---")
            print(r["text"])

if __name__ == "__main__":
    main()