import boto3
from botocore.client import Config
from ..config import settings
import os

class R2Service:
    def __init__(self):
        self.s3_client = boto3.client(
            service_name='s3',
            endpoint_url=f'https://{settings.CLOUDFLARE_R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = settings.CLOUDFLARE_R2_BUCKET_NAME
        self.public_url_base = settings.CLOUDFLARE_R2_PUBLIC_URL

    def upload_file(self, local_file_path: str, destination_blob_name: str):
        """Uploads a file to the R2 bucket."""
        try:
            self.s3_client.upload_file(
                local_file_path,
                self.bucket_name,
                destination_blob_name
            )
            # Construct the public URL
            return f"{self.public_url_base}/{destination_blob_name}"
        except Exception as e:
            print(f"Error uploading to R2: {e}")
            return None

r2_service = R2Service()
