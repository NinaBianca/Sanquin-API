from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from datetime import datetime
from .enums import DonationType
from ..database import Base

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String, nullable=False)
    type = Column(Enum(DonationType), nullable=False)
    amount = Column(Float, nullable=False)
    appointment = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False)
