from sqlalchemy import Column, Integer, ForeignKey, String, func
from sqlalchemy.ext.hybrid import hybrid_property
from .donation import Donation
from database import Base

class ChallengeUser(Base):
    __tablename__ = "challenge_users"

    challenge_id = Column(Integer, ForeignKey("challenges.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    status = Column(String, nullable=False)  # 'pending', 'active', 'completed'

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
