from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func

class Bookmarks(Base):
    __tablename__ = "bookmarks"

    bookmark_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id = mapped_column(Integer, ForeignKey('posts.post_id', ondelete="CASCADE"))
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_details = relationship("UserDetails", back_populates="bookmarks")
    posts = relationship("Posts", back_populates="bookmarks")

    def serialize(self, full=True):
        data = {
            'bookmark_id': self.bookmark_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'account_id': self.user_details.account_id,
            'user_name': self.user_details.user_name
        }
        if full:
            post_user_name = self.posts.user_details.user_name if self.posts and self.posts.user_details else None
            data.update({
                'created_at': self.created_at,
                'content': self.posts.content if self.posts else None,
                'post_user_name': post_user_name    
            })
        return data
    
    def __repr__(self):
        return f'<Bookmarks {self.bookmark_id}>'