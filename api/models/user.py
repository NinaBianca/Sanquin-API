from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .enums import UserRole
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    birthdate = Column(DateTime, nullable=False)
    city = Column(String, nullable=False)
    points = Column(Integer, default=0)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.now)

    # Relationship to donations
    donations = relationship("Donation", backref="user", lazy="dynamic")
    
    # Relationship to challenges (all challenges linked to user)
    challenges = relationship("Challenge", secondary="challenge_users", backref="participants", lazy="dynamic")

    def model_dump(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate,
            "city": self.city,
            "points": self.points,
            "role": self.role,
            "created_at": self.created_at
        }
