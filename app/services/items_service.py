
from sqlalchemy.orm import Session
from ..models import database, schemas

def get_item(db: Session, item_id: int):
    return db.query(database.Item).filter(database.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = database.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def search_items(db: Session, query: str):
    # Basic keyword search for now
    # Semantic search would require vector similarity search on embeddings
    return db.query(database.Item).filter(database.Item.summary.contains(query) | database.Item.transcription.contains(query)).all()
