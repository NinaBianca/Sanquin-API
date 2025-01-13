from sqlalchemy import Column, Integer, ForeignKey, Enum, func, between
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Session
from .donation import Donation
from .enums import ChallengeStatus
from ..database import Base


class ChallengeUser(Base):
    __tablename__ = "challenge_users"

    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    status = Column(Enum(ChallengeStatus), nullable=False)  

    challenge = relationship("Challenge", back_populates="participants")
    user = relationship("User", back_populates="challenges")

