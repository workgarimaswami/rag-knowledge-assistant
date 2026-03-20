# 🧠 RAG Knowledge Assistant

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![RAG](https://img.shields.io/badge/Architecture-RAG-8A2BE2)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
[![LLM](https://img.shields.io/badge/Powered%20by-LLM-FF6B6B)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A **Retrieval-Augmented Generation (RAG)** system that transforms your documents into an intelligent, queryable knowledge base — enabling accurate, context-aware answers grounded in your own data.

---

## 📌 Overview

The **RAG Knowledge Assistant** combines the power of large language models with semantic document retrieval to answer questions based on your custom knowledge sources. Unlike standard LLMs, this system grounds its responses in your actual documents — eliminating hallucinations and ensuring answers are always relevant and traceable.

### Why RAG?

| Standard LLM | RAG Knowledge Assistant |
|---|---|
| Answers from training data only | Answers from *your* documents |
| May hallucinate facts | Grounded in retrieved context |
| Static knowledge cutoff | Always up-to-date with your data |
| No source attribution | Cites source documents |

---

## 🏗️ Architecture

```
                        ┌─────────────────────────────────────┐
                        │           RAG Pipeline              │
                        │                                     │
  Your Documents ──────►│  INGESTION                          │
  (PDF, TXT, etc.)      │  ├── Load & parse documents         │
                        │  ├── Chunk text                     │
                        │  └── Embed & store in vector DB     │
                        │            │                        │
  User Query ──────────►│  RETRIEVAL                          │
                        │  ├── Embed query                    │
                        │  ├── Similarity search              │
                        │  └── Fetch top-k relevant chunks    │
                        │            │                        │
                        │  API / LLM                          │
                        │  ├── Augment prompt with context    │
                        │  └── Generate grounded answer       │
                        └─────────────────────────────────────┘
                                      │
                               Answer + Sources
```

---

## 📁 Project Structure

```
rag-knowledge-assistant/
│
├── api/                    # REST API layer
│   ├── app.py              #   FastAPI / Flask application
│   ├── routes.py           #   Endpoint definitions
│   └── schemas.py          #   Request / response models
│
├── ingestion/              # Document ingestion pipeline
│   ├── loader.py           #   Document loaders (PDF, TXT, DOCX, web)
│   ├── chunker.py          #   Text chunking strategies
│   └── embedder.py         #   Embedding generation & vector storage
│
├── retrieval/              # Semantic retrieval engine
│   ├── retriever.py        #   Vector similarity search
│   ├── reranker.py         #   Result reranking
│   └── generator.py        #   LLM response generation with context
│
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **API** | FastAPI / Flask |
| **Embeddings** | OpenAI `text-embedding-ada-002` / HuggingFace |
| **Vector Store** | FAISS / ChromaDB / Pinecone |
| **LLM** | OpenAI GPT-4 / GPT-3.5 |
| **Document Parsing** | LangChain / LlamaIndex |
| **Containerization** | Docker + Docker Compose |
| **Language** | Python 3.9+ |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- OpenAI API key (or compatible LLM provider)

### 1. Clone the Repository

```bash
git clone https://github.com/workgarimaswami/rag-knowledge-assistant.git
cd rag-knowledge-assistant
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
VECTOR_STORE=faiss          # faiss | chroma | pinecone
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-4
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Ingest Your Documents

```bash
python ingestion/loader.py --source ./documents/
```

### 5. Start the API

```bash
python api/app.py
```

API available at `http://localhost:8000`.

---

## 🐳 Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

Services started:
- `api` — REST API on port `8000`
- `vector-db` — Vector store on port `6333` (if using ChromaDB)

---

## 🔌 API Reference

### Ingest Documents

**POST** `/ingest`

```json
{
  "source": "path/to/document.pdf",
  "metadata": { "category": "finance", "author": "Jane Doe" }
}
```

### Ask a Question

**POST** `/query`

```json
{
  "question": "What are the key findings from the Q3 report?",
  "top_k": 5
}
```

**Response:**

```json
{
  "answer": "According to the Q3 report, revenue grew by 23% year-over-year...",
  "sources": [
    { "document": "q3_report.pdf", "page": 4, "relevance_score": 0.94 }
  ]
}
```

### Health Check

**GET** `/health` → `{ "status": "ok", "documents_indexed": 142 }`

---

## 🔧 Configuration

| Parameter | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | `500` | Token size per document chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between consecutive chunks |
| `TOP_K` | `5` | Number of retrieved chunks per query |
| `VECTOR_STORE` | `faiss` | Backend vector store |
| `LLM_MODEL` | `gpt-4` | Language model for generation |

---

## 📂 Supported Document Types

- 📄 PDF (`.pdf`)
- 📝 Plain text (`.txt`)
- 📋 Word documents (`.docx`)
- 🌐 Web URLs
- 📊 Markdown (`.md`)
- 🗂️ CSV / JSON

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🗺️ Roadmap

- [ ] Multi-modal support (images, tables)
- [ ] Streaming responses
- [ ] Conversation memory / chat history
- [ ] Web UI / chat interface
- [ ] Support for multiple vector store backends
- [ ] Document versioning and update tracking

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Garima Swami** · [@workgarimaswami](https://github.com/workgarimaswami)

---

⭐ *If this project helped you build something awesome, give it a star!*
