🏙️ Real Estate Research Tool – AI-Powered Insight Engine
<h3 align="center">🏡 Simplify Real Estate Insights with AI</h3> <p align="center"> An intelligent assistant that scrapes real estate news, transforms it into searchable knowledge using embeddings and vector databases, and answers your questions using Llama-3 via Groq. </p>
🌟 Overview

This project is a domain-specific AI research assistant built for real estate analysts, investors, and enthusiasts.
It combines web scraping, semantic vector search, and retrieval-augmented generation (RAG) to extract and answer insights from real-estate articles.

⚙️ Core Workflow

Scrape – Pulls content from URLs using LangChain’s WebBaseLoader.

Split – Breaks content into manageable chunks using RecursiveCharacterTextSplitter.

Embed – Converts text into dense vectors using HuggingFaceEmbeddings.

Store – Saves embeddings in a persistent ChromaDB vectorstore.

Query – Answers user questions using Llama-3 (Groq) with citations from the indexed articles.

🧱 Tech Stack
Component	Library / Tool	Description
🧠 LLM	Llama-3 (Groq API)	Generates intelligent, contextual answers
🧩 Framework	LangChain	Orchestration framework for RAG pipelines
💾 Vector DB	Chroma	Lightweight vector database for embeddings
🔍 Embeddings	Sentence-Transformers / HuggingFace	Creates semantic text representations
🌐 Web Loader	LangChain-Community WebBaseLoader	Fetches and parses web content
🌱 Config	python-dotenv	Handles API keys securely
🎯 Interface	Streamlit (optional)	Simple web app for user interaction
🧩 Installation & Setup

Clone the Repository

git clone https://github.com/<your-github-username>/real-estate-assistant.git
cd real-estate-assistant


Install Dependencies

pip install -r requirements.txt


Set Environment Variables
Create a .env file in your project root:

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile


Run the Script

python main.py

🚀 How It Works
1️⃣ Process URLs

The script loads one or multiple URLs, scrapes their content, and stores semantic embeddings inside resources/vectorstore/.

urls = [
    "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
    "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
]
process_urls(urls)

2️⃣ Ask a Question

After embeddings are stored, query them:

question = "Tell me what was the 30-year fixed mortgage rate along with the date?"
answer, sources = generate_answer(question)


✅ Sample Output

Question: Tell me what was the 30-year fixed mortgage rate along with the date?
Answer: The 30-year fixed mortgage rate rose to 6.9% on Dec 20, 2024...
Sources: https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html

🖥️ Optional Streamlit UI

If you want a graphical interface:

streamlit run app.py


You can paste multiple article links in the sidebar, process them, and ask questions interactively.

🧰 File Structure
real-estate-assistant/
│
├── main.py                     # Core script (RAG pipeline)
├── resources/
│   ├── vectorstore/             # Persistent Chroma vector DB
│   └── image.png                # Screenshot / demo image
├── .env                         # Your Groq credentials
├── requirements.txt
└── README.md

📚 Dependencies (requirements.txt)
langchain==0.3.7
langchain-community==0.3.29
langchain-chroma==0.2.5
langchain-groq==0.3.7
langchain-huggingface==0.3.1
python-dotenv==1.1.0
sentence-transformers==5.0.0
nltk==3.9.1
streamlit==1.45.0
requests==2.32.5

🔒 Notes / Troubleshooting

If you get

TypeError: 'NoneType' object is not iterable


→ Replace any for status in process_urls(urls): with

process_urls(urls)


If nltk download fails, your script already handles it silently with SSL overrides.

Vectorstore data is persisted under resources/vectorstore. You can delete it to start fresh.

🤝 Contributing

Pull requests and enhancements are welcome.
If you extend this project to other domains (finance, healthcare, supply chain), please document your domain-specific modifications clearly.

🪪 License

Copyright (C) CodeBasics Inc.
Licensed under the MIT License.
Commercial use is prohibited without prior written permission.
Attribution is required in derivative works.
