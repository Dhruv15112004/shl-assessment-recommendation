import pandas as pd

from recommender.search import SHLRecommender
from recommender.ranker import balanced_ranking


DATASET_PATH = "Gen_AI Dataset.xlsx"
OUTPUT_PATH = "predictions.csv"
TOP_K = 10


def generate_predictions():
    print("📥 Loading dataset...")
    df = pd.read_excel(DATASET_PATH)

    recommender = SHLRecommender()

    rows = []

    print("🔮 Generating predictions...\n")

    for idx, row in df.iterrows():
        query = row["Query"]

        raw_results = recommender.search(query, top_k=20)
        final_results = balanced_ranking(query, raw_results, final_k=TOP_K)

        urls = [r.get("url", "") for r in final_results]

        rows.append({
            "Query": query,
            "Recommended_Assessment_URLs": ",".join(urls)
        })

        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(df)} queries")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print("\n✅ predictions.csv generated successfully!")


if __name__ == "__main__":
    generate_predictions()
