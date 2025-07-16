from typing import Optional
from fastapi import APIRouter, File, UploadFile, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from ...models import schemas
from ...services import items_service
from ...dependencies import get_db
from ...services.tasks import process_image_upload, process_audio_upload, process_text_upload
import os
import tempfile

router = APIRouter()

UPLOAD_DIR = "storage/uploads"

@router.post("/", response_model=schemas.Item)
async def upload_all(image: Optional[UploadFile] = File(None),
                       audio: Optional[UploadFile] = File(None),
                       note: Optional[str] = Form(None),
                       db: Session = Depends(get_db)):
    
    if not (image or audio or note):
        raise HTTPException(status_code=400, detail="At least one of image, audio, or note must be provided.")

    # Create a placeholder item immediately
    placeholder_item_data = {"type": "mixed", "transcription": "Processing...", "summary": "Processing..."}
    if image: placeholder_item_data["type"] = "image"
    elif audio: placeholder_item_data["type"] = "audio"
    elif note: placeholder_item_data["type"] = "note"

    placeholder_item = items_service.create_item(db=db, item=schemas.ItemCreate(**placeholder_item_data))
    item_id = placeholder_item.id

    if image:
        image_upload_dir = os.path.join(UPLOAD_DIR, "images")
        os.makedirs(image_upload_dir, exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, dir=image_upload_dir) as tmp_image:
            tmp_image.write(await image.read())
            image_path = tmp_image.name
        process_image_upload.delay(image_path, item_id)

    if audio:
        audio_upload_dir = os.path.join(UPLOAD_DIR, "audio")
        os.makedirs(audio_upload_dir, exist_ok=True)
        file_extension = os.path.splitext(audio.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, dir=audio_upload_dir) as tmp_audio:
            tmp_audio.write(await audio.read())
            audio_path = tmp_audio.name
        process_audio_upload.delay(audio_path, item_id)

    if note:
        process_text_upload.delay(note, item_id)

    return placeholder_item
