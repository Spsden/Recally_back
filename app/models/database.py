
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.mutable import MutableList
from ..database import Base
from datetime import datetime

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, default=1)  # Default user_id for now
    type = Column(String, index=True)
    transcription = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    tags = Column(MutableList.as_mutable(JSON), nullable=True)
    actionables = Column(MutableList.as_mutable(JSON), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding = Column(MutableList.as_mutable(JSON), nullable=True)
