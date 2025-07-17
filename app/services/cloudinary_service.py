import cloudinary
import cloudinary.uploader
from ..config import settings
import os

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    def upload_image(self, file_path: str, public_id: str = None):
        """Uploads an image to Cloudinary."""
        try:
            response = cloudinary.uploader.upload(file_path, public_id=public_id)
            return response['secure_url']
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            return None

cloudinary_service = CloudinaryService()
