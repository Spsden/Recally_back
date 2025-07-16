
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...models import schemas
from ...services import items_service
from ...dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = items_service.get_items(db, skip=skip, limit=limit)
    return items
