import firebase_admin
from firebase_admin import credentials, storage
from ..config import settings
import os

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred, {
                'storageBucket': settings.FIREBASE_STORAGE_BUCKET
            })
        self.bucket = storage.bucket()

    def upload_file(self, local_file_path: str, destination_blob_name: str):
        """Uploads a file to the Firebase Storage bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)
        blob.make_public()
        return blob.public_url

firebase_service = FirebaseService()
