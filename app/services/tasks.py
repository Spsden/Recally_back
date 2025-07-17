from ..core.celery_app import celery_app
from ..services import llm_service, items_service
from ..services.cloudinary_service import cloudinary_service
from ..models import schemas
from ..database import SessionLocal
import os
import json
import redis
from ..config import settings

# Initialize Redis client for publishing
redis_publisher = redis.from_url(settings.REDIS_URL, decode_responses=True)

@celery_app.task
def process_image_upload(file_path: str, item_id: int):
    db = SessionLocal()
    try:
        item = items_service.get_item(db, item_id)
        if not item:
            print(f"Item with ID {item_id} not found.")
            return

        ocr_text = llm_service.ocr_image(file_path)
        summary, tags, actionables = llm_service.summarize_text(ocr_text)

        # Upload image to Firebase Storage
        file_name = os.path.basename(file_path)
        r2_url = r2_service.upload_file(file_path, f"processed_images/{file_name}")

        item.transcription = ocr_text
        item.summary = summary
        item.tags = tags
        item.actionables = actionables
        item.image_url = r2_url
        db.add(item)
        db.commit()
        db.refresh(item)

        # Publish update to Redis Pub/Sub
        updated_item_data = schemas.Item.from_orm(item).json()
        redis_publisher.publish("item_updates", json.dumps({"item_id": item.id, "item_data": json.loads(updated_item_data)}))

    finally:
        db.close()
    os.remove(file_path)

@celery_app.task
def process_audio_upload(file_path: str, item_id: int):
    db = SessionLocal()
    try:
        item = items_service.get_item(db, item_id)
        if not item:
            print(f"Item with ID {item_id} not found.")
            return

        transcription = llm_service.transcribe_audio(file_path)
        summary, tags, actionables = llm_service.summarize_text(transcription)

        item.transcription = transcription
        item.summary = summary
        item.tags = tags
        item.actionables = actionables
        db.add(item)
        db.commit()
        db.refresh(item)

        # Publish update to Redis Pub/Sub
        updated_item_data = schemas.Item.from_orm(item).json()
        redis_publisher.publish("item_updates", json.dumps({"item_id": item.id, "item_data": json.loads(updated_item_data)}))

    finally:
        db.close()
    os.remove(file_path)

@celery_app.task
def process_text_upload(text_content: str, item_id: int):
    db = SessionLocal()
    try:
        item = items_service.get_item(db, item_id)
        if not item:
            print(f"Item with ID {item_id} not found.")
            return

        summary, tags, actionables = llm_service.summarize_text(text_content)

        item.transcription = text_content
        item.summary = summary
        item.tags = tags
        item.actionables = actionables
        db.add(item)
        db.commit()
        db.refresh(item)

        # Publish update to Redis Pub/Sub
        updated_item_data = schemas.Item.from_orm(item).json()
        redis_publisher.publish("item_updates", json.dumps({"item_id": item.id, "item_data": json.loads(updated_item_data)}))

    finally:
        db.close()
