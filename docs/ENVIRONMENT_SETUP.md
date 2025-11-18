# Environment and Dependencies Setup

This document describes how to set up the development environment and manage dependencies.

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Virtual Environment**: Recommended for isolation

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- At least **one** API key: `OPENAI_API_KEY`, `GROQ_API_KEY`, or `GOOGLE_API_KEY`

Optional variables:
- `CHROMA_COLLECTION_NAME`: Vector database collection name (default: `rag_documents`)
- `EMBEDDING_MODEL`: Embedding model name (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `OPENAI_MODEL`: OpenAI model name (default: `gpt-4o-mini`)
- `GROQ_MODEL`: Groq model name (default: `llama-3.1-8b-instant`)
- `GOOGLE_MODEL`: Google model name (default: `gemini-2.0-flash`)

## Virtual Environment Setup

### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Dependency Management

### Core Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **LangChain**: LLM orchestration framework
- **ChromaDB**: Vector database
- **Sentence Transformers**: Embedding models

### LLM Provider Dependencies

Install based on your chosen provider:
- `langchain-openai`: For OpenAI models
- `langchain-groq`: For Groq models
- `langchain-google-genai`: For Google Gemini models

### Development Dependencies (Optional)

```bash
pip install -e ".[dev]"
```

Includes:
- `black`: Code formatter
- `flake8`: Linter
- `mypy`: Type checker
- `pytest`: Testing framework

## Dependency Updates

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To generate updated requirements:

```bash
pip freeze > requirements.txt
```

## Troubleshooting

### NumPy Compatibility Issues

If you encounter NumPy 2.x compatibility issues:

```bash
pip install "numpy<2" "protobuf<=4.25.3" "googleapis-common-protos<=1.63.2"
```

### TensorFlow Issues

If TensorFlow import errors occur, ensure compatible versions:

```bash
pip install "tensorflow==2.15.1"
```

## Platform-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Path separators: `\` or `/` both work
- Virtual environment activation: `venv\Scripts\activate`

### Linux/Mac

- Use bash or zsh
- Path separators: `/`
- Virtual environment activation: `source venv/bin/activate`

