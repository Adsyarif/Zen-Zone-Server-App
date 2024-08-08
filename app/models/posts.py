from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

class Posts(Base):
    __tablename__ = "posts"

    post_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    content = mapped_column(String)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now(), ondelete=func.now())

    user_details = relationship("User_details", back_populates="posts")
    bookmarks = relationship("Bookmarks", back_populates="posts")
    like = relationship("Like", back_populates="posts")
    comments = relationship("Comments", back_populates="posts")
    report_post = relationship("Report_post", back_populates="posts")


    def serialize(self, full=True):
        data = {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at
        }
        if full:
            data.update({
                'deleted_at': self.deleted_at
            })
        return data
    
    def __repr__(self):
        return f'<Post {self.post_id}>'