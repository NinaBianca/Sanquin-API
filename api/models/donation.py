from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from datetime import datetime, UTC
from .enums import DonationType
from ..database import Base

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location_id = Column(Integer, ForeignKey("location_info.id"))
    type = Column(Enum(DonationType), nullable=False)
    amount = Column(Float, nullable=True, default=0.0)
    appointment = Column(DateTime, nullable=False, default=datetime.now(UTC))
    status = Column(String, nullable=False)

    
