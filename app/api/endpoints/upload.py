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

    if image:
        image_upload_dir = os.path.join(UPLOAD_DIR, "images")
        os.makedirs(image_upload_dir, exist_ok=True)
        file_extension = os.path.splitext(image.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, dir=image_upload_dir) as tmp_image:
            tmp_image.write(await image.read())
            image_path = tmp_image.name
        process_image_upload.delay(image_path)
        return schemas.Item(type="image", transcription="Processing...", summary="Processing...", tags=[], actionables=[])

    if audio:
        audio_upload_dir = os.path.join(UPLOAD_DIR, "audio")
        os.makedirs(audio_upload_dir, exist_ok=True)
        file_extension = os.path.splitext(audio.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, dir=audio_upload_dir) as tmp_audio:
            tmp_audio.write(await audio.read())
            audio_path = tmp_audio.name
        process_audio_upload.delay(audio_path)
        return schemas.Item(type="audio", transcription="Processing...", summary="Processing...", tags=[], actionables=[])

    if note:
        process_text_upload.delay(note)
        return schemas.Item(type="text", transcription=note, summary="Processing...", tags=[], actionables=[])


# Remove the old /image/ endpoint as it's now handled by upload_all
# @router.post("/image/", response_model=schemas.Item)
# async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if not os.path.exists(f"{UPLOAD_DIR}/images"):
#         os.makedirs(f"{UPLOAD_DIR}/images")
#     file_path = os.path.join(f"{UPLOAD_DIR}/images", file.filename)
#     with open(file_path, "wb") as buffer:
#         buffer.write(await file.read())

#     ocr_text = llm_service.ocr_image(file_path)
#     summary, tags, actionables = llm_service.summarize_text(ocr_text)

#     item = schemas.ItemCreate(
#         type="image",
#         transcription=ocr_text, # Store OCR text in transcription field
#         summary=summary,
#         tags=tags,
#         actionables=actionables,
#     )
#     return items_service.create_item(db=db, item=item)