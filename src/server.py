import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.app import RAGAssistant, load_documents


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(3, ge=1, le=10, description="Number of context chunks to retrieve")


class SourceItem(BaseModel):
    source: Optional[str] = None
    file_path: Optional[str] = None
    chunk_index: Optional[int] = None
    distance: Optional[float] = None
    excerpt: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    context: Optional[str] = None
    sources: List[SourceItem] = Field(default_factory=list)


BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"
UPLOAD_DIR = (BASE_DIR.parent / "uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Research RAG Assistant", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

assistant: Optional[RAGAssistant] = None
assistant_lock = asyncio.Lock()


async def bootstrap_assistant() -> RAGAssistant:
    global assistant
    if assistant:
        return assistant

    async with assistant_lock:
        if assistant:
            return assistant

        rag_assistant = RAGAssistant()
        documents = load_documents()
        if documents:
            rag_assistant.add_documents(documents)
        else:
            print("Warning: No documents were loaded. Upload files to the data directory.")

        assistant = rag_assistant
        return assistant


@app.on_event("startup")
async def on_startup() -> None:
    await bootstrap_assistant()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health", response_model=Dict[str, Any])
async def healthcheck():
    return {"status": "ok"}


@app.post("/api/query", response_model=QueryResponse)
async def query_rag(payload: QueryRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please provide a question.")

    rag_assistant = await bootstrap_assistant()

    result = rag_assistant.query(
        question,
        n_results=payload.top_k,
        include_context=True,
    )

    if isinstance(result, str):
        return QueryResponse(answer=result)

    return QueryResponse(
        answer=result.get("answer", ""),
        context=result.get("context"),
        sources=[SourceItem(**source) for source in result.get("sources", [])],
    )


@app.post("/api/upload", response_model=Dict[str, Any])
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required.")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".txt"}:
        raise HTTPException(status_code=400, detail="Only .txt files are currently supported.")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        text = contents.decode("utf-8", errors="ignore")

    unique_name = f"{Path(file.filename).stem}_{uuid4().hex[:8]}{suffix}"
    saved_path = UPLOAD_DIR / unique_name
    saved_path.write_text(text, encoding="utf-8")

    rag_assistant = await bootstrap_assistant()
    chunks_added = rag_assistant.add_documents(
        [
            {
                "content": text,
                "metadata": {"source": file.filename, "file_path": str(saved_path)},
            }
        ]
    )

    if chunks_added == 0:
        raise HTTPException(
            status_code=400,
            detail="The file could not be processed into searchable chunks.",
        )

    return {
        "status": "ok",
        "message": f"Uploaded '{file.filename}' and added {chunks_added} new chunks to the knowledge base.",
        "filename": file.filename,
        "chunks_added": chunks_added,
    }

