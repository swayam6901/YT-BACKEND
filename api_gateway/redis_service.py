import os
import redis

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(redis_url)

def enqueue_job(job_id, job_data):
    r.rpush("summarizer_jobs", job_data)