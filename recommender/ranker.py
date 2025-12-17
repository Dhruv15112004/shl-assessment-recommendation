import re

def detect_query_intent(query):
    query = query.lower()

    technical_keywords = [
        "java", "python", "sql", "developer", "coding",
        "technical", "software", "engineer"
    ]

    behavioral_keywords = [
        "collaborate", "communication", "team",
        "stakeholder", "leadership", "personality"
    ]

    intent = {
        "technical": any(k in query for k in technical_keywords),
        "behavioral": any(k in query for k in behavioral_keywords)
    }

    return intent


def balanced_ranking(query, retrieved_results, final_k=10):
    intent = detect_query_intent(query)

    technical = []
    behavioral = []
    general = []

    for r in retrieved_results:
        types = r.get("test_type_normalized", [])

        if "Knowledge" in types:
            technical.append(r)
        elif "Personality" in types or "Cognitive" in types:
            behavioral.append(r)
        else:
            general.append(r)

    final_results = []

    # If query requires both, enforce balance
    if intent["technical"] and intent["behavioral"]:
        while len(final_results) < final_k:
            if technical:
                final_results.append(technical.pop(0))
            if behavioral:
                final_results.append(behavioral.pop(0))
            if not technical and not behavioral:
                break

    else:
        final_results = technical + behavioral + general

    # Fill remaining slots
    for r in general:
        if len(final_results) < final_k:
            final_results.append(r)

    return final_results[:final_k]
