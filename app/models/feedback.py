from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func, Float

from datetime import timezone, timedelta

JAKARTA_TZ = timezone(timedelta(hours=7))
class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))
    description = mapped_column(String)
    rating = mapped_column(Float)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    def serialize(self, full=True):
        data = {
            'feedback_id': self.feedback_id,
            'account_id': self.account_id, 
            'description': self.description,
            'rating': self.rating,
            'created_at': self.created_at.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
        if full:
            data.update ({
                'updated_at': self.updated_at.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
                'deleted_at': self.deleted_at.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.deleted_at else None
            })
        return data
    
    def __repr__(self):
        return f'<Feedback{self.feedback_id}>'