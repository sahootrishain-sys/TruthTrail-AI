import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from search import search_web

# Load .env for local development
load_dotenv()

# Use Streamlit secrets if deployed, otherwise use .env
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

client = genai.Client(api_key=api_key)

st.title("🕵️ TruthTrail AI")
st.subheader("OSINT Investigation Agent")

query = st.text_input("What would you like to investigate?")

if st.button("Investigate") and query:

    with st.spinner("Searching the web..."):
        results = search_web(query)

    context = ""

    for r in results:
        context += f"""
Title: {r['title']}
Summary: {r['body']}
URL: {r['href']}

"""

    prompt = f"""
You are a professional OSINT investigator.

Using ONLY the evidence below, create a detailed investigation report.

Question:
{query}

Evidence:
{context}

Your report must contain:

1. Executive Summary

2. Key Findings

3. Supporting Evidence

4. Possible Risks or Unknowns

5. Confidence Score (0-100%)

6. Final Conclusion
"""

    with st.spinner("Analyzing evidence..."):
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

    st.success("Investigation Complete!")

    st.markdown(response.text)

    st.divider()

    st.subheader("Sources")

    for r in results:
        st.write(f"🔹 **{r['title']}**")
        st.write(r["href"])