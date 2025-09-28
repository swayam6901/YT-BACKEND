import os
import firebase_admin
from firebase_admin import credentials, firestore

firebase_creds = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": "dummy",
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": "dummy",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "dummy"
}

cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

def set_job_status(job_id, status, summary=None, error=None):
    db.collection('jobs').document(job_id).set({
        'status': status,
        'summary': summary,
        'error': error
    }, merge=True)

def get_job_status(job_id):
    doc = db.collection('jobs').document(job_id).get()
    if doc.exists:
        return doc.to_dict()
    return None