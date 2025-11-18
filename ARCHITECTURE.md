# Architecture Documentation

This document describes the architecture and structure of the RAG-Based AI Assistant project.

## System Overview

The RAG (Retrieval-Augmented Generation) system combines:
- **Document Storage**: ChromaDB vector database for semantic search
- **Embeddings**: Sentence Transformers for text embeddings
- **LLM Integration**: LangChain with support for multiple providers
- **Web Interface**: FastAPI backend with vanilla JavaScript frontend

## Repository Structure

```
RAG_Based_AI_Asst/
├── src/                    # Source code
│   ├── app.py             # Main RAG assistant logic
│   ├── server.py          # FastAPI web server
│   ├── vectordb.py        # Vector database wrapper
│   ├── static/            # Frontend assets
│   │   ├── app.js         # Client-side JavaScript
│   │   └── styles.css     # Styling
│   └── templates/         # HTML templates
│       └── index.html     # Main UI template
├── data/                  # Initial document storage
├── uploads/               # User-uploaded documents
├── chroma_db/            # ChromaDB persistent storage
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── LICENSE               # License file
└── README.md             # Project documentation
```

## Component Architecture

### 1. RAGAssistant (`src/app.py`)

The core RAG system that:
- Initializes LLM (OpenAI/Groq/Google)
- Manages vector database connection
- Implements RAG query pipeline:
  1. Query embedding generation
  2. Similarity search in vector DB
  3. Context retrieval and combination
  4. LLM response generation

### 2. VectorDB (`src/vectordb.py`)

Handles:
- Document chunking using LangChain's RecursiveCharacterTextSplitter
- Embedding generation with Sentence Transformers
- ChromaDB collection management
- Similarity search operations

### 3. Web Server (`src/server.py`)

FastAPI application providing:
- REST API endpoints (`/api/query`, `/api/upload`)
- Static file serving
- HTML template rendering
- CORS middleware

### 4. Frontend (`src/static/`)

Vanilla JavaScript SPA with:
- Chat interface
- Document upload functionality
- Real-time status updates
- Error handling

## Data Flow

1. **Document Ingestion**:
   ```
   Document → Chunking → Embedding → ChromaDB Storage
   ```

2. **Query Processing**:
   ```
   User Query → Embedding → Similarity Search → Context Retrieval → LLM → Response
   ```

## Technology Stack

- **Backend**: Python 3.10+, FastAPI
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **LLM Framework**: LangChain
- **LLM Providers**: OpenAI, Groq, Google Gemini
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

## Configuration

Environment variables (see `.env.example`):
- API keys for LLM providers
- Optional: Collection name, embedding model

## Dependencies

See `requirements.txt` for complete list. Key dependencies:
- `fastapi`: Web framework
- `langchain`: LLM orchestration
- `chromadb`: Vector database
- `sentence-transformers`: Embeddings
- `langchain-openai`, `langchain-groq`, `langchain-google-genai`: LLM providers

