import pandas as pd
import re

INPUT_PATH = "data/raw/shl_assessments_raw.csv"
OUTPUT_PATH = "data/processed/shl_assessments_clean.csv"

def normalize_test_type(text, name="", description=""):
    combined = f"{text} {name} {description}".lower()

    categories = []

    if any(k in combined for k in [
        "java", "python", "sql", "coding", "programming",
        "technical", "software", "developer", "skill"
    ]):
        categories.append("Knowledge")

    if any(k in combined for k in [
        "personality", "behavior", "behaviour",
        "opq", "motivation", "judgement", "sjt"
    ]):
        categories.append("Personality")

    if any(k in combined for k in [
        "cognitive", "ability", "numerical",
        "verbal", "logical", "reasoning"
    ]):
        categories.append("Cognitive")

    return categories if categories else ["General"]


def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def main():
    df = pd.read_csv(INPUT_PATH)

    # Drop rows with missing names or URLs
    df = df.dropna(subset=["name", "url"])

    # Clean text fields
    df["name"] = df["name"].apply(clean_text)
    df["description"] = df["description"].apply(clean_text)

    # Normalize test types
    df["test_type_normalized"] = df.apply(
    lambda r: normalize_test_type(
        r.get("test_type", ""),
        r.get("name", ""),
        r.get("description", "")
    ),
    axis=1
)

    # Keep only required columns
    final_df = df[
        ["name", "url", "description", "test_type_normalized",
         "duration", "remote_support", "adaptive_support"]
    ]

    final_df.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Clean dataset saved: {OUTPUT_PATH}")
    print(f"📊 Total clean assessments: {len(final_df)}")

if __name__ == "__main__":
    main()
