import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/embeddings/shl_faiss.index"
META_PATH = "data/embeddings/shl_metadata.pkl"


class SHLRecommender:
    def __init__(self):
        print("🔄 Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("📂 Loading metadata...")
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        print("🧠 Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query: str, top_k: int = 20):
        """
        Perform semantic search using FAISS.
        Returns raw retrieved assessment records (NO ranking here).
        """
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.metadata[idx])

        return results


# Local test (optional, safe)
if __name__ == "__main__":
    recommender = SHLRecommender()

    test_query = "Hiring a Java developer who can collaborate with business teams"
    results = recommender.search(test_query, top_k=5)

    print("\n🔍 Top Retrieved Assessments:\n")
    for r in results:
        print(f"- {r['name']} | {r['url']} | {r['test_type_normalized']}")
