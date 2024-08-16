from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

class ReportPost(Base):
    __tablename__ = "report_post"

    report_post_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_category_id = mapped_column(Integer, ForeignKey('report_category.report_category_id', ondelete="CASCADE"))
    report_content = mapped_column(String)
    post_id = mapped_column(Integer, ForeignKey('posts.post_id', ondelete="CASCADE"))
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
  
    posts = relationship("Posts", back_populates="report_post")
    user_details = relationship("UserDetails", back_populates="report_post")
    report_category = relationship("ReportCategory", back_populates="report_post")

    def serialize(self, full=True):
        data = {
            'report_post_id': self.report_post_id,
            'report_category_id': self.report_category.serialize() if self.report_category else None,
            'report_content': self.report_content,
            'post_id': self.post_id,
            'user_id': self.user_id
            
        }
        if full:
            data.update({
                'created_at': self.created_at,
                'account_id':self.user_details.account_id
            })
        return data
    
    def __repr__(self):
        return f'<Report_post {self.report_post_id}>'