# @Author: Dhaval Patel | Modified by Keerthi Amulya Madireddy
# Copyrights Codebasics Inc. and LearnerX Pvt Ltd.

from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path
import ssl
import nltk
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# ---------------------------------------------------------------------
# INITIAL SETUP
# ---------------------------------------------------------------------
load_dotenv()

# fix SSL issue for nltk downloads
ssl._create_default_https_context = ssl._create_unverified_context

# download required nltk resources
for resource in ["punkt", "averaged_perceptron_tagger", "punkt_tab"]:
    try:
        nltk.download(resource, quiet=True)
    except Exception as e:
        print(f"⚠️ Warning: Failed to download {resource}: {e}")

# ---------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------
CHUNK_SIZE = 1000
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

# ---------------------------------------------------------------------
# GLOBAL OBJECTS
# ---------------------------------------------------------------------
llm = None
vector_store = None

# ---------------------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------------------
def initialize_components():
    """
    Initialize LLM and vector store once.
    """
    global llm, vector_store

    if llm is None:
        yield "Initializing LLM...✅"
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=500)

    if vector_store is None:
        yield "Initializing Vector Database...✅"
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


# ---------------------------------------------------------------------
# DATA INGESTION & EMBEDDING (YIELD VERSION)
# ---------------------------------------------------------------------
def process_urls(urls):
    """
    Stream status updates while scraping and embedding URLs.
    Perfect for Streamlit live feedback.
    """
    yield "Starting data ingestion...✅"

    # Initialize
    yield from initialize_components()

    yield "Resetting vector store...✅"
    vector_store.reset_collection()

    yield "Loading data from URLs...✅"
    loader = WebBaseLoader(urls)

    try:
        data = loader.load()
        if not data:
            yield "⚠️ No content extracted from URLs. Please verify accessibility."
            return
    except Exception as e:
        yield f"⚠️ Error loading URLs: {e}"
        return

    yield "Splitting text into chunks...✅"
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE
    )
    docs = text_splitter.split_documents(data)

    if not docs:
        yield "⚠️ No valid text chunks generated. Skipping embedding."
        return

    yield f"Adding {len(docs)} chunks to vector database...✅"
    try:
        uuids = [str(uuid4()) for _ in range(len(docs))]
        vector_store.add_documents(docs, ids=uuids)
        vector_store.persist()
        yield "Persisted vector database successfully!✅"
    except Exception as e:
        yield f"⚠️ Error while embedding docs: {e}"
        return

    yield "🎉 Data ingestion complete! You can now ask questions."


# ---------------------------------------------------------------------
# QUERY HANDLER
# ---------------------------------------------------------------------
def generate_answer(query):
    """
    Generate an answer for a given user query using RAG pipeline.
    """
    global llm, vector_store

    if not vector_store:
        yield from initialize_components()

    yield f"Running query: {query}"
    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever()
    )

    result = chain.invoke({"question": query}, return_only_outputs=True)
    answer = result.get("answer", "No answer found.")
    sources = result.get("sources", "No sources found.")
    yield f"Answer: {answer}"
    yield f"Sources: {sources}"


# ---------------------------------------------------------------------
# MAIN EXECUTION (Optional for standalone testing)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]

    for step in process_urls(urls):
        print(step)

    for output in generate_answer("Tell me what was the 30-year fixed mortgage rate along with the date?"):
        print(output)