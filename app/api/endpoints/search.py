
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...models import schemas
from ...services import items_service
from ...dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Item])
def search_items(q: str, db: Session = Depends(get_db)):
    items = items_service.search_items(db, query=q)
    return items
