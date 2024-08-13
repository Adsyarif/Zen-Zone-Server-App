from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func

class Comments(Base):
    __tablename__ = "comments"

    comment_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id = mapped_column(Integer, ForeignKey('posts.post_id', ondelete="CASCADE"))
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    content = mapped_column(String)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_details = relationship("UserDetails", back_populates="comments")
    posts = relationship("Posts", back_populates="comments")
    report_comment = relationship("ReportComment", back_populates="comments")

    def serialize(self, full=True):
        data = {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at,
            'user_name': self.user_details.user_name,
            'account_id': self.user_details.account_id
        }
        if full:
            data.update({
                'deleted_at': self.deleted_at
            })
        return data
    
    def __repr__(self):
        return f'<Comments {self.comment_id}>'