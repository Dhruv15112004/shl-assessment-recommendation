from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from recommender.search import SHLRecommender
from recommender.ranker import balanced_ranking

app = FastAPI(title="SHL Assessment Recommendation API")

# Load recommender once at startup
recommender = SHLRecommender()


# ---------- Request / Response Models ----------

class RecommendRequest(BaseModel):
    query: str
    top_k: int = 5


class AssessmentResponse(BaseModel):
    name: str
    url: str
    test_type: List[str]
    description: Optional[str] = None
    duration: Optional[str] = None
    remote_support: Optional[str] = None
    adaptive_support: Optional[str] = None


# ---------- Utility helpers (VERY IMPORTANT) ----------

def safe_list(value):
    """
    Ensures test_type is always a list of strings.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        return [value]
    return []


def safe_str(value):
    """
    Converts nan / None to None, otherwise string.
    """
    if value is None:
        return None
    if str(value).lower() == "nan":
        return None
    return str(value)


# ---------- Endpoints ----------

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    try:
        # 1. Retrieve
        raw_results = recommender.search(req.query, top_k=20)

        # 2. Rank
        final_results = balanced_ranking(
            req.query,
            raw_results,
            final_k=req.top_k
        )

        # 3. Clean JSON-safe response
        response = []
        for r in final_results:
            response.append({
                "name": safe_str(r.get("name")),
                "url": safe_str(r.get("url")),
                "test_type": safe_list(r.get("test_type_normalized")),
                "description": safe_str(r.get("description")),
                "duration": safe_str(r.get("duration")),
                "remote_support": safe_str(r.get("remote_support")),
                "adaptive_support": safe_str(r.get("adaptive_support")),
            })

        return {"recommended_assessments": response}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
