import pandas as pd
from recommender.search import SHLRecommender
from recommender.ranker import balanced_ranking


DATASET_PATH = "Gen_AI Dataset.xlsx"
TOP_K = 10


def evaluate_recall_at_k():
    print("📥 Loading dataset...")
    df = pd.read_excel(DATASET_PATH)

    recommender = SHLRecommender()

    hits = 0
    total = len(df)

    print(f"🔍 Evaluating Recall@{TOP_K} on {total} queries...\n")

    for idx, row in df.iterrows():
        query = row["Query"]
        true_url = row["Assessment_url"]

        # Step 1: retrieve candidates
        raw_results = recommender.search(query, top_k=20)

        # Step 2: rank
        final_results = balanced_ranking(
            query,
            raw_results,
            final_k=TOP_K
        )

        # Step 3: collect predicted URLs
        predicted_urls = [r["url"] for r in final_results]

        # Step 4: check hit
        if true_url in predicted_urls:
            hits += 1

        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{total} queries")

    recall = hits / total
    print("\n==============================")
    print(f"✅ Recall@{TOP_K}: {recall:.4f}")
    print("==============================")

    return recall


if __name__ == "__main__":
    evaluate_recall_at_k()
