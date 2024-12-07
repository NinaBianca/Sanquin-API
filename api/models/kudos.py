from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Kudos(Base):
    __tablename__ = "kudos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    # Relationship to Post
    post = relationship("Post", back_populates="kudos_list")

    def __repr__(self):
        return f"<Kudos(id={self.id}, user_id={self.user_id}, post_id={self.post_id})>"
