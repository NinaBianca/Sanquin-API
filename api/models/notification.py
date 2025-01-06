from database import Base 
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    retrieved = Column(Boolean, default=False)
