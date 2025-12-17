import pandas as pd
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/processed/shl_assessments_clean.csv"
INDEX_PATH = "data/embeddings/shl_faiss.index"
META_PATH = "data/embeddings/shl_metadata.pkl"

def main():
    print("📥 Loading clean dataset...")
    df = pd.read_csv(DATA_PATH)

    # Prepare text for embedding
    texts = []
    for _, row in df.iterrows():
        combined = f"""
        Assessment Name: {row['name']}
        Description: {row['description']}
        Test Type: {row['test_type_normalized']}
        """
        texts.append(combined.strip())

    print("🧠 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔢 Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")
    dim = embeddings.shape[1]

    print("📦 Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("💾 Saving FAISS index...")
    faiss.write_index(index, INDEX_PATH)

    print("💾 Saving metadata...")
    with open(META_PATH, "wb") as f:
        pickle.dump(df.to_dict(orient="records"), f)

    print(f"✅ FAISS index built with {index.ntotal} vectors")

if __name__ == "__main__":
    main()
