from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .enums import FriendshipStatus
from ..database import Base

class Friend(Base):
    __tablename__ = "friends"

    sender_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
