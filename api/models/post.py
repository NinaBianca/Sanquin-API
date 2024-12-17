from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)

    # Relationship to User (who created the post)
    user = relationship("User", backref="posts")

    # Relationship to Kudos (likes on the post)
    kudos_list = relationship("Kudos", back_populates="post", lazy="dynamic")

    def __repr__(self):
        return f"<Post(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"
