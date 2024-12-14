from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from .challenge_user import ChallengeUser
from .donation import Donation
from database import Base

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    goal = Column(Float, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    # Hybrid property to calculate total contributions (participant donations)
    @hybrid_property
    def total(self):
        from sqlalchemy.orm import Session
        session = Session.object_session(self)
        total_contributions = (
            session.query(func.sum(Donation.amount))
            .join(ChallengeUser, Donation.user_id == ChallengeUser.user_id)
            .filter(
                ChallengeUser.challenge_id == self.id,
                Donation.appointment.between(self.start, self.end)
            )
            .scalar()
        )
        return total_contributions or 0.0
