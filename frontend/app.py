import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🔍 SHL Assessment Recommendation System")

API_URL = "https://shl-assessment-api-ipbi.onrender.com/recommend"

query = st.text_area(
    "Enter Job Description or Hiring Query",
    height=150,
    placeholder="e.g. Hiring a Java developer who can collaborate with stakeholders"
)

top_k = st.slider("Number of recommendations", 1, 10, 5)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        payload = {
            "query": query,
            "top_k": top_k
        }

        try:
            with st.spinner("Fetching recommendations..."):
                response = requests.post(API_URL, json=payload, timeout=30)

            # Debug output (keep this for now)
            st.write("Status code:", response.status_code)
            st.write("Raw response:", response.text)

            if response.status_code == 200:
                data = response.json()
                results = data.get("recommended_assessments", [])

                if results:
                    df = pd.DataFrame(results)
                    st.success("Recommendations generated!")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No recommendations returned.")
            else:
                st.error("API Error. Please check backend.")

        except Exception as e:
            st.error(f"Request failed: {e}")
