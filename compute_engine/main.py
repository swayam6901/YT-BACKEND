import os
import time
import redis
import json
from firebase_service import set_job_status
from transcription import transcribe_video
from summarization import generate_summary

def process_job(job_id, job_data):
    try:
        video_url = job_data.get("video_url")
        summary_type = job_data.get("summary_type", "short")
        
        set_job_status(job_id, "transcribing")
        transcript = transcribe_video(video_url)
        
        set_job_status(job_id, "summarizing")
        summary = generate_summary(transcript, summary_type)
        
        set_job_status(job_id, "completed", summary=summary)
        return {"summary": summary}
        
    except Exception as e:
        error_msg = str(e)
        set_job_status(job_id, "error", error=error_msg)
        return {"error": error_msg}

if __name__ == "__main__":
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    r = redis.from_url(redis_url)
    print("Compute Engine started. Waiting for jobs...")
    while True:
        job = r.blpop("summarizer_jobs", timeout=10)
        if job:
            _, job_data = job
            job_data = json.loads(job_data)
            job_id = job_data.get("job_id")
            result = process_job(job_id, job_data)
            print(f"Job result: {result}")
        else:
            time.sleep(1)