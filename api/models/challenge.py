from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func, select, between
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from .challenge_user import ChallengeUser
from .donation import Donation
from ..database import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    goal = Column(Float, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    reward_points = Column(Integer, nullable=False, default=0)

    participants = relationship("ChallengeUser", back_populates="challenge", cascade="all, delete-orphan")
