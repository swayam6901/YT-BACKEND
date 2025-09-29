from http.server import BaseHTTPRequestHandler
from ..transcription import transcribe_video
from ..summarization import generate_summary
from ..firebase_service import set_job_status
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        job_id = data.get('job_id')
        video_url = data.get('video_url')
        summary_type = data.get('summary_type', 'short')
        
        try:
            set_job_status(job_id, "transcribing")
            transcript = transcribe_video(video_url)
            
            set_job_status(job_id, "summarizing")
            summary = generate_summary(transcript, summary_type)
            
            set_job_status(job_id, "completed", summary=summary)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
        except Exception as e:
            error_msg = str(e)
            set_job_status(job_id, "error", error=error_msg)
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": error_msg}).encode())