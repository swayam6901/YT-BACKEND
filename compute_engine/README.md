# Compute Engine (AI Execution)

This is the deploy-ready compute engine for the YouTube AI Summarizer project.

## Deployment (Render Background Worker)

1. **Repository Setup:**
   - Push this folder to your GitHub repository.

2. **Create a new Background Worker on Render:**
   - Select your repository and the `compute_engine` directory as the root.
   - Set the build command to:
     ```
     pip install -r requirements.txt
     ```
   - Set the start command to:
     ```
     python main.py
     ```

3. **Environment Variables:**
   - Add any required environment variables (see `.env.example`).

4. **Production Ready:**
   - No local-only scripts or dev dependencies are included.
   - All dependencies are listed in `requirements.txt`.

## Notes
- Integrate transcription and summarization logic in the next steps.
- This service is ready for direct deployment on Render as a background worker.