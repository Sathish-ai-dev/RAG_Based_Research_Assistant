# RAG-Based AI Assistant - AAIDC Project 1 Template

## 🤖 What is this?

This is a **learning template** for building a RAG (Retrieval-Augmented Generation) AI assistant. RAG systems combine document search with AI chat - they can answer questions about your specific documents by finding relevant information and using it to generate responses.

**Think of it as:** ChatGPT that knows about YOUR documents and can answer questions about them.

## 🎯 What you'll build

By completing this project, you'll have an AI assistant that can:

- 📄 **Load your documents** (PDFs, text files, etc.)
- 🔍 **Search through them** to find relevant information
- 💬 **Answer questions** using the information it found
- 🧠 **Combine multiple sources** to give comprehensive answers


Welcome to your RAG (Retrieval-Augmented Generation) project! This repository provides a **template** that you need to complete. The framework is set up, but the core functionality is missing - that's your job to implement!

## 🎯 What You Need to Build

You will implement a complete RAG system that can:

- Load and chunk documents from the `data/` directory
- Create embeddings and store them in a vector database
- Search for relevant context based on user queries
- Generate responses using retrieved context and an LLM


## 📝 Implementation Steps

The project requires implementing 7 main steps:

1. **Prepare Your Documents** - Add your own documents to the data directory
2. **Document Loading** - Load documents from files into the system
3. **Text Chunking** - Split documents into smaller, searchable chunks
4. **Document Ingestion** - Process and store documents in the vector database  
5. **Similarity Search** - Find relevant documents based on queries
6. **RAG Prompt Template** - Design effective prompts for the LLM
7. **RAG Query Pipeline** - Complete query-response pipeline using retrieved context

---

### Step 1: Prepare Your Documents

**Replace the sample documents with your own content**

The `data/` directory contains sample files on various topics. Replace these with documents relevant to your domain:

```
data/
├── your_topic_1.txt
├── your_topic_2.txt
└── your_topic_3.txt
```

Each file should contain text content you want your RAG system to search through.

---

### Step 2: Implement Document Loading

**Location:** `src/app.py`

```python
def load_documents() -> List[str]:
    """
    Load documents for demonstration.

    Returns:
        List of sample documents
    """
    results = []
    # TODO: Implement document loading
    # HINT: Read the documents from the data directory
    # HINT: Return a list of documents
    # HINT: Your implementation depends on the type of documents you are using (.txt, .pdf, etc.)

    # Your implementation here
    return results
```

**What you need to do:**

- Read files from the `data/` directory
- Load the content of each file into memory
- Return a list of document dictionaries with content and metadata
- You implementation should handle the type of files you are using (text, pdf, etc)

**Key considerations:**

- Use `os.listdir()` or `glob.glob()` to find files in the data directory
- Read file contents using appropriate encoding (usually 'utf-8')
- Create document dictionaries with 'content' and 'metadata' fields
- Handle errors gracefully (missing files, encoding issues, etc.)

---

### Step 3: Implement Text Chunking

**Location:** `src/vectordb.py`

```python
def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
    """
    Split text into smaller chunks for better retrieval.
  
    Args:
        text: Input text to chunk
        chunk_size: Approximate number of characters per chunk
  
    Returns:
        List of text chunks
    """
    # TODO: Your implementation here
```

**What you need to do:**

- Choose a chunking strategy (word-based, sentence-based, or use LangChain's text splitters)
- Split the input text into manageable chunks
- Return a list of text strings

**Hint:** You have multiple options - start simple with word-based splitting or explore LangChain's `RecursiveCharacterTextSplitter`.

---

### Step 4: Implement Document Ingestion

**Location:** `src/vectordb.py`

```python
def add_documents(self, documents: List[Dict[str, Any]]) -> None:
    """
    Process documents and add them to the vector database.
  
    Args:
        documents: List of documents with 'content' and optional 'metadata'
    """
    # TODO: Your implementation here
```

**What you need to do:**

- Loop through the documents list
- Extract content and metadata from each document
- Use your `chunk_text()` method to split documents
- Create embeddings using `self.embedding_model.encode()`
- Store everything in ChromaDB using `self.collection.add()`

**Key components:**

- Chunk each document's content
- Generate unique IDs for each chunk
- Create embeddings for all chunks
- Store in the vector database

---

### Step 5: Implement Similarity Search

**Location:** `src/vectordb.py`

```python
def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
    """
    Find documents similar to the query.
  
    Args:
        query: Search query
        n_results: Number of results to return
  
    Returns:
        Dictionary with search results
    """
    # TODO: Your implementation here
```

**What you need to do:**

- Create an embedding for the query using `self.embedding_model.encode()`
- Search the ChromaDB collection using `self.collection.query()`
- Return results in the expected format with keys: `documents`, `metadatas`, `distances`, `ids`

---

### Step 6: Implement RAG Prompt Template

**Location:** `src/app.py`

```python
# Create RAG prompt template
# TODO: Implement your RAG prompt template
# HINT: Use ChatPromptTemplate.from_template() with a template string
# HINT: Your template should include placeholders for {context} and {question}
# HINT: Design your prompt to effectively use retrieved context to answer questions
self.prompt_template = None  # Your implementation here
```

**What you need to do:**

- Design a prompt template that effectively combines retrieved context with user questions
- Use `ChatPromptTemplate.from_template()` to create the template
- Include placeholders for `{context}` (retrieved documents) and `{question}` (user query)
- Consider how to instruct the LLM to use the context appropriately
- Handle cases where the context might not contain relevant information

**Key considerations:**

- Clear instructions for the AI on how to use the retrieved context
- Guidance on what to do when context is insufficient or irrelevant
- Consistent formatting that works well with your chosen LLM
- Balance between being specific enough to be helpful and flexible enough to handle various queries

---

### Step 7: Implement RAG Query Pipeline

**Location:** `src/app.py`

```python
def query(self, question: str, n_results: int = 3) -> Dict[str, Any]:
    """
    Answer questions using retrieved context.
  
    Args:
        question: User's question
        n_results: Number of context chunks to retrieve
  
    Returns:
        Dictionary with answer and context information
    """
    # TODO: Your implementation here
```

**What you need to do:**

- Use `self.vector_db.search()` to find relevant context
- Combine retrieved chunks into a context string
- Use `self.chain.invoke()` to generate a response
- Return a dictionary with the answer and metadata

**The RAG pipeline:**

1. Search for relevant chunks
2. Combine chunks into context
3. Generate response using LLM + context
4. Return structured results


---

## 🧪 Testing Your Implementation

### Test Individual Components

1. **Test chunking:**

   ```python
   from src.vectordb import VectorDB
   vdb = VectorDB()
   chunks = vdb.chunk_text("Your test text here...")
   print(f"Created {len(chunks)} chunks")
   ```
2. **Test document loading:**

   ```python
   documents = [{"content": "Test document", "metadata": {"title": "Test"}}]
   vdb.add_documents(documents)
   ```
3. **Test search:**

   ```python
   results = vdb.search("your test query")
   print(f"Found {len(results['documents'])} results")
   ```

### Test Full System

Once implemented, run:

```bash
python src/app.py
```

Try these example questions:

- "What is [topic from your documents]?"
- "Explain [concept from your documents]"
- "How does [process from your documents] work?"

---

## 🌐 Optional Web Interface

You can interact with the assistant through a lightweight FastAPI + HTML interface:

```bash
uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000` in your browser. The UI provides:

- A clean chat surface for your questions and answers
- Live request status messaging
- One-click upload support for adding new plain-text research notes without leaving the browser

This UI uses the same `RAGAssistant` under the hood, so any documents you add to `data/` automatically power both the CLI and web experiences.

### Uploading new research files

- Use the upload bar at the top of the web UI to send `.txt` documents.
- Each file is chunked, embedded, and added to the persistent Chroma collection immediately.
- After a successful upload, you can ask questions about the new material right away—no restart required.

---

## 🔧 Implementation Freedom

**Important:** This template uses specific packages (ChromaDB, LangChain, HuggingFace Transformers) and approaches, but **you are completely free to use whatever you prefer!**

### Alternative Options You Can Choose:

**Vector Databases:**
- FAISS (Facebook AI Similarity Search)
- Pinecone
- Weaviate
- Qdrant
- Or any other vector store you prefer

**LLM Frameworks:**
- Direct API calls (OpenAI, Anthropic, etc.)
- Ollama for local models
- Hugging Face Transformers
- LlamaIndex instead of LangChain

**Embedding Models:**
- OpenAI embeddings (ada-002)
- Cohere embeddings
- Any Hugging Face model
- Local embedding models

**Text Processing:**
- Custom chunking logic
- spaCy for advanced NLP
- NLTK for text processing
- Your own parsing methods

---

## 🚀 Setup Instructions

### Prerequisites

Before starting, make sure you have:

- Python 3.8 or higher installed
- An API key from **one** of these providers:
  - [OpenAI](https://platform.openai.com/api-keys) (most popular)
  - [Groq](https://console.groq.com/keys) (free tier available)
  - [Google AI](https://aistudio.google.com/app/apikey) (competitive pricing)

### Quick Setup

1. **Clone and install dependencies:**

   ```bash
   git clone [your-repo-url]
   cd rt-aaidc-project1-template
   pip install -r requirements.txt
   ```

2. **Configure your API key:**

   ```bash
   # Create environment file (choose the method that works on your system)
   cp .env.example .env    # Linux/Mac
   copy .env.example .env  # Windows
   ```

   Edit `.env` and add your API key:

   ```
   OPENAI_API_KEY=your_key_here
   # OR
   GROQ_API_KEY=your_key_here  
   # OR
   GOOGLE_API_KEY=your_key_here
   ```


---

## 📁 Project Structure

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
│   └── *.txt             # Research documents
├── uploads/               # User-uploaded documents
├── chroma_db/            # ChromaDB persistent storage
├── docs/                  # Additional documentation
│   ├── CODE_QUALITY.md   # Code quality standards
│   └── ENVIRONMENT_SETUP.md  # Environment setup guide
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .env.example          # Environment variable template
├── .flake8               # Flake8 linting configuration
├── LICENSE               # License file (CC BY-NC-SA 4.0)
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md          # Version history
├── ARCHITECTURE.md        # Architecture documentation
└── README.md             # This guide
```

---

## 🎓 Learning Objectives

By completing this project, you will:

- ✅ Understand RAG architecture and data flow
- ✅ Implement text chunking strategies
- ✅ Work with vector databases and embeddings
- ✅ Build LLM-powered applications with LangChain
- ✅ Handle multiple API providers
- ✅ Create production-ready AI applications

---

## 🏁 Success Criteria

Your implementation is complete when:

1. ✅ You can load your own documents
2. ✅ The system chunks and embeds documents
3. ✅ Search returns relevant results
4. ✅ The RAG system generates contextual answers
5. ✅ You can ask questions and get meaningful responses

**Good luck building your RAG system! 🚀**

---

## 📚 Additional Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture and design decisions
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Guidelines for contributing to the project
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and changes
- **[docs/CODE_QUALITY.md](docs/CODE_QUALITY.md)**: Code quality standards and best practices
- **[docs/ENVIRONMENT_SETUP.md](docs/ENVIRONMENT_SETUP.md)**: Detailed environment setup guide

## 📄 License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. See [LICENSE](LICENSE) for details.

## 🏗️ Framework Organization

This project follows a structured framework with five main categories:

1. **Documentation**: Comprehensive guides, architecture docs, and contribution guidelines
2. **Repository Structure**: Well-organized directory structure with clear separation of concerns
3. **Environment and Dependencies**: Clear setup instructions, dependency management, and configuration
4. **License and Legal**: CC BY-NC-SA 4.0 license with proper attribution requirements
5. **Code Quality**: Type hints, docstrings, linting, formatting standards, and best practices
