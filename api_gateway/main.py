from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="YouTube AI Summarizer API Gateway")

from .firebase_service import set_job_status, get_job_status
from .redis_service import enqueue_job

class SummarizeRequest(BaseModel):
    video_url: str
    summary_type: str  # 'short' or 'detailed'

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    summary: Optional[str] = None
    error: Optional[str] = None

@app.post("/summarize", response_model=JobStatusResponse)
def submit_summarization(req: SummarizeRequest):
    job_id = str(uuid.uuid4())
    set_job_status(job_id, "queued")
    enqueue_job(job_id, req.json())
    return JobStatusResponse(job_id=job_id, status="queued")

@app.get("/status/{job_id}", response_model=JobStatusResponse)
def get_status(job_id: str):
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(job_id=job_id, status=job.get("status"), summary=job.get("summary"), error=job.get("error"))