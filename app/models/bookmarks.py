from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func

class Bookmarks(Base):
    __tablename__ = "bookmarks"

    bookmark_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id = mapped_column(Integer, ForeignKey('posts.post_id', ondelete="CASCADE"))
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_details = relationship("User_details", back_populates="bookmarks")
    posts = relationship("Posts", back_populates="bookmarks")

    def serialize(self, full=True):
        data = {
            'bookmark_id': self.bookmark_id,
            'post_id': self.post_id,
            'user_id': self.user_id
        }
        if full:
            data.update({
                'created_at': self.created_at
            })
        return data
    
    def __repr__(self):
        return f'<Bookmarks {self.bookmark_id}>'