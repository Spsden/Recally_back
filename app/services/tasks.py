from ..core.celery_app import celery_app
from ..services import llm_service, items_service
from ..models import schemas
from ..database import SessionLocal
import os

@celery_app.task
def process_image_upload(file_path: str):
    db = SessionLocal()
    try:
        ocr_text = llm_service.ocr_image(file_path)
        summary, tags, actionables = llm_service.summarize_text(ocr_text)

        item = schemas.ItemCreate(
            type="image",
            transcription=ocr_text,
            summary=summary,
            tags=tags,
            actionables=actionables,
        )
        items_service.create_item(db=db, item=item)
    finally:
        db.close()
    os.remove(file_path)

@celery_app.task
def process_audio_upload(file_path: str):
    db = SessionLocal()
    try:
        transcription = llm_service.transcribe_audio(file_path)
        summary, tags, actionables = llm_service.summarize_text(transcription)

        item = schemas.ItemCreate(
            type="audio",
            transcription=transcription,
            summary=summary,
            tags=tags,
            actionables=actionables,
        )
        items_service.create_item(db=db, item=item)
    finally:
        db.close()
    os.remove(file_path)

@celery_app.task
def process_text_upload(text_content: str):
    db = SessionLocal()
    try:
        summary, tags, actionables = llm_service.summarize_text(text_content)

        item = schemas.ItemCreate(
            type="text",
            transcription=text_content,
            summary=summary,
            tags=tags,
            actionables=actionables,
        )
        items_service.create_item(db=db, item=item)
    finally:
        db.close()
