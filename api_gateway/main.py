import os
import uuid
import httpx
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from firebase_service import set_job_status, get_job_status, get_pending_jobs

class SummarizeRequest(BaseModel):
    video_url: str
    summary_type: str  # 'short' or 'detailed'

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    summary: Optional[str] = None
    error: Optional[str] = None

app = FastAPI(title="YouTube AI Summarizer API Gateway")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize", response_model=JobStatusResponse)
async def submit_summarization(req: SummarizeRequest):
    job_id = str(uuid.uuid4())
    set_job_status(job_id, "queued")
    
    # Process job immediately
    vercel_url = os.getenv("VERCEL_FUNCTION_URL")
    if not vercel_url:
        raise HTTPException(status_code=500, detail="Vercel function URL not configured")
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                vercel_url,
                json={
                    "job_id": job_id,
                    "video_url": req.video_url,
                    "summary_type": req.summary_type
                },
                timeout=30.0
            )
            if response.status_code != 200:
                set_job_status(job_id, "error", error=f"Vercel function returned status {response.status_code}")
                raise HTTPException(status_code=500, detail=f"Vercel function returned status {response.status_code}")
    except Exception as e:
        set_job_status(job_id, "error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
    return JobStatusResponse(job_id=job_id, status="queued")

@app.get("/status/{job_id}", response_model=JobStatusResponse)
def get_status(job_id: str):
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(job_id=job_id, status=job.get("status"), summary=job.get("summary"), error=job.get("error"))
