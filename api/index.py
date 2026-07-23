from fastapi import FastAPI
from pydantic import BaseModel

from src.app import RAGAssistant

app = FastAPI(title="RAG Research Assistant")

assistant = RAGAssistant()


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "RAG Research Assistant API"
    }


@app.post("/query")
def query(data: Query):
    answer = assistant.query(data.question)
    return {
        "question": data.question,
        "answer": answer
    }