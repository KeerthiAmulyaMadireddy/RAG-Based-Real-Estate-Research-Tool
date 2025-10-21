# @Author: Dhaval Patel | Modified by Keerthi Amulya Madireddy
# Copyrights Codebasics Inc. and LearnerX Pvt Ltd.

import streamlit as st
from rag import process_urls, generate_answer

# ---------------------------------------------------------------------
# APP TITLE
# ---------------------------------------------------------------------
st.set_page_config(page_title="Real Estate Research Tool", page_icon="🏠", layout="wide")
st.title("🏠 Real Estate Research Tool")

# ---------------------------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------------------------
st.sidebar.header("🔗 Enter Research URLs")
url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

placeholder = st.empty()

# ---------------------------------------------------------------------
# PROCESS URLS BUTTON
# ---------------------------------------------------------------------
process_url_button = st.sidebar.button("🚀 Process URLs")
if process_url_button:
    urls = [url for url in (url1, url2, url3) if url.strip() != ""]
    if len(urls) == 0:
        placeholder.warning("⚠️ You must provide at least one valid URL.")
    else:
        placeholder.info("Processing URLs... please wait ⏳")
        for status in process_urls(urls):
            placeholder.text(status)
        placeholder.success("✅ Data ingestion complete! You can now ask questions below.")

# ---------------------------------------------------------------------
# QUESTION INPUT
# ---------------------------------------------------------------------
st.divider()
st.subheader("💬 Ask a Question about the Articles")

query = st.text_input("Enter your question here:")

if query:
    try:
        # Stream updates from generate_answer
        answer_placeholder = st.empty()
        sources_placeholder = st.empty()

        for output in generate_answer(query):
            if output.startswith("Answer:"):
                answer_placeholder.subheader("🧠 Answer")
                answer_placeholder.write(output.replace("Answer:", "").strip())
            elif output.startswith("Sources:"):
                sources_placeholder.subheader("📚 Sources")
                for src in output.replace("Sources:", "").strip().split("\n"):
                    if src.strip():
                        sources_placeholder.write(f"- {src.strip()}")
            else:
                answer_placeholder.text(output)

    except RuntimeError:
        st.error("⚠️ Please process URLs first before asking questions.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")