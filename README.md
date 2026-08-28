<div align="center">

# 🎬 TubeTalk AI

### Turn Long YouTube Videos into Instant, Searchable Knowledge.

<p>
  <code>YouTube</code> → <code>Transcript</code> → <code>Chunks</code> → <code>Embeddings</code> → <code>ChromaDB</code> → <code>RAG</code> → <code>Llama 3.2</code>
</p>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F61?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Ollama](https://img.shields.io/badge/Ollama-Llama_3.2-black?style=for-the-badge)

</div>

---

## ⚡ What is TubeTalk AI?

**TubeTalk AI** is a high-performance **Retrieval-Augmented Generation (RAG)** backend that lets you ask natural-language questions about any YouTube video. No need to watch long tutorials or podcasts—just drop the link and start chatting!

`🎥 YouTube URL` ➔ `📝 Transcribe & Chunk` ➔ `🗄️ Store in ChromaDB` ➔ `🔎 Semantic Search` ➔ `🤖 Llama 3.2 Answer`

---

## 🚀 Key Features

* 🎥 **Instant Video Ingestion:** Automatically extracts transcripts (supports English & Hindi).
* ✂️ **Smart Semantic Chunking:** Splits transcripts using `RecursiveCharacterTextSplitter`.
* 🧠 **Vector Search:** Converts text into embeddings via `all-MiniLM-L6-v2` & stores them in **ChromaDB**.
* 🦙 **100% Local LLM Privacy:** Powered by **Ollama** running **Llama 3.2** locally.
* ⚡ **FastAPI Backend:** Fully asynchronous, clean, and developer-friendly REST endpoints.

---

## 🛠️ Tech Stack

| Domain | Tools / Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.x, FastAPI, Uvicorn |
| **RAG & Vector Storage** | ChromaDB, LangChain Splitters, Hugging Face Transformers |
| **LLM Orchestration** | Ollama (Llama 3.2) |
| **Transcript Source** | YouTube Transcript API |

---

## 📁 Project Structure

```text
TubeTalk-AI/
├── 📁 services/
│   ├── 📝 chunk_extractor.py
│   ├── 🧠 embadding.py
│   ├── 🔎 query.py
│   └── 🦙 ollama_connection.py
├── 🗄️ chroma_db/
├── 🚀 app.py
├── ⚙️ config.py
├── 🗃️ database.py
├── 📦 requirements.txt
└── 🔒 .env
```

---

## ⚡ Quick Start Guide

### 1️⃣ Clone & Setup Virtual Environment

```bash
git clone https://github.com/ytsubhadip/TubeTalk-AI.git
cd TubeTalk-AI

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure `.env`

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
```

### 4️⃣ Pull Local Model (Ollama)

Make sure Ollama is installed and running:

```bash
ollama pull llama3.2
```

### 5️⃣ Run the API

```bash
uvicorn app:app --reload
```

> 🌐 **Interactive API Docs:** Open `http://127.0.0.1:8000/docs` in your browser.

---

## 🔌 API Endpoints Cheat Sheet

| Method | Endpoint | Description | Sample Payload |
| :--- | :--- | :--- | :--- |
| `POST` | `/youtube_url` | Ingest transcript into ChromaDB | `{"url": "https://youtu.be/VIDEO_ID"}` |
| `POST` | `/query` | Ask a question about an ingested video | `{"video_id": "VIDEO_ID", "query": "What is the key takeaway?"}` |

---

## 🤝 Contributing & Support

Contributions are always welcome! Feel free to **Fork**, create a feature branch, and submit a **Pull Request**.

If you like this project, don't forget to give it a ⭐ on GitHub!

<div align="center">

**WATCH LESS. ASK MORE. LEARN FASTER.**

*Built with ❤️ using FastAPI, ChromaDB, and Ollama.*

</div>
