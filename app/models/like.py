from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func

class Like(Base):
    __tablename__ = "like"

    like_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id = mapped_column(Integer, ForeignKey('posts.post_id', ondelete="CASCADE"))
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_details = relationship("UserDetails", back_populates="like")
    posts = relationship("Posts", back_populates="like")

    def serialize(self, full=True):
        data = {
            'like_id': self.like_id,
            'post_id': self.post_id,
            'user_id': self.user_id
        }
        if full:
            data.update({
                'created_at': self.created_at
            })
        return data
    
    def __repr__(self):
        return f'<Like {self.like_id}>'