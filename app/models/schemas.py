from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from typing import Literal

class ItemBase(BaseModel):
    type: Literal["audio", "image", "note", "mixed"]
    transcription: Optional[str] = None
    summary: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    actionables: List[Dict[str, Any]] = Field(default_factory=list)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    user_id: int
    created_at: datetime
    embedding: Optional[List[float]] = Field(default_factory=list)

    class Config:
        orm_mode = True
