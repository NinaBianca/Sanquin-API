from sqlalchemy import Column, Integer, ForeignKey, Enum, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from .donation import Donation
from .enums import ChallengeStatus
from database import Base

class ChallengeUser(Base):
    __tablename__ = "challenge_users"

    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    status = Column(Enum(ChallengeStatus), nullable=False)  

    challenge = relationship("Challenge", back_populates="participants")
    user = relationship("User", back_populates="challenges")

    # Hybrid property for calculating the user's total donations during the challenge period
    @hybrid_property
    def total(self):
        from sqlalchemy.orm import Session
        session = Session.object_session(self)
        user_donations = (
            session.query(func.sum(Donation.amount))
            .filter(
                Donation.user_id == self.user_id,
                Donation.appointment.between(self.challenge.start, self.challenge.end)
            )
            .scalar()
        )
        return user_donations or 0.0
