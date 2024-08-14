from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

class ReportComment(Base):
    __tablename__ = "report_comment"

    report_comment_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_category_id = mapped_column(Integer, ForeignKey('report_category.report_category_id', ondelete="CASCADE"))
    report_content = mapped_column(String)
    comment_id = mapped_column(Integer, ForeignKey('comments.comment_id', ondelete="CASCADE"))
    user_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
  
    comments = relationship("Comments", back_populates="report_comment")
    user_details = relationship("UserDetails", back_populates="report_comment")
    report_category = relationship("ReportCategory", back_populates="report_comment")


    def serialize(self, full=True):
        data = {
            'report_comment_id': self.report_comment_id,
            'report_category_id': self.report_category.serialize() if self.report_category else None,
            'report_content': self.report_content,
            'comment_id': self.comment_id,
            'user_id': self.user_id,
            'account_id':self.user_details.account_id
        }
        if full:
            data.update({
                'created_at': self.created_at
            })
        return data
    
    def __repr__(self):
        return f'<Report_comment {self.report_comment_id}>'