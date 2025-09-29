# API Gateway (Task Dispatcher)

This is the deploy-ready FastAPI gateway for the YouTube AI Summarizer project.

## Deployment (Render)

1. **Repository Setup:**
   - Push this folder to your GitHub repository.

2. **Create a new Web Service on Render:**
   - Select your repository and the `api_gateway` directory as the root.
   - Set the build command to:
     ```
     pip install -r requirements.txt
     ```
   - Set the start command to:
     ```
     uvicorn main:app --host 0.0.0.0 --port 10000
     ```
   - (You can change the port as needed.)

3. **Environment Variables:**
   - Add any required environment variables (see `.env.example`).

4. **Production Ready:**
   - No local-only scripts or dev dependencies are included.
   - All dependencies are listed in `requirements.txt`.

## Endpoints
- `POST /summarize` — Submit a YouTube URL and summary type. Returns a Job ID.
- `GET /status/{job_id}` — Check job status and retrieve results.

## Notes
- Integrate Firebase and task queue in the next steps.
- This service is ready for direct deployment on Render.