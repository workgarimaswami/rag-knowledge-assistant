import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from typing import List
import redis.asyncio as redis
from dotenv import load_dotenv

from ingestion.pipeline import ingest_file
from retrieval.chain import rag_chain

load_dotenv()

app = FastAPI(title="enterprise knowledge assistant")

# ----- Request/Response Models -----
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    relevance_scores: List[float]

# ----- Startup Event: Initialize Redis Cache -----
@app.on_event("startup")
async def startup():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

# ----- Endpoints -----
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a document (PDF, DOCX, MD, CSV) to be ingested."""
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ingest the file
        ingest_file(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return {"message": f"File '{file.filename}' ingested successfully"}

@app.post("/query", response_model=QueryResponse)
@cache(expire=300)  # Cache for 5 minutes
async def query_endpoint(request: QueryRequest):
    """Ask a question and get an answer with sources."""
    try:
        result = rag_chain(request.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))