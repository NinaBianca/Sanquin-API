from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .enums import DonationType, DonationStatus
from database import Base

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    location_id = Column(Integer, ForeignKey("location_info.id", ondelete="SET NULL"))
    donation_type = Column(Enum(DonationType), nullable=False)
    amount = Column(Float, nullable=True, default=0.0)
    appointment = Column(DateTime, nullable=False, default=datetime.now(UTC))
    status = Column(Enum(DonationStatus), nullable=False)

    user = relationship("User", back_populates="donations")
    location = relationship("LocationInfo", back_populates="donations")
