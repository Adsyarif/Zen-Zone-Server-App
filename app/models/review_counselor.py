from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from datetime import timezone, timedelta

JAKARTA_TZ = timezone(timedelta(hours=7))

class ReviewCounselor(Base):
    __tablename__ = "review_counselor"

    review_counselor_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    content = mapped_column(String)
    created_at = mapped_column(DateTime(timezone=True), default=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.null())
    account_id = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))
    account_id_counselor = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))

    account = relationship("Account", back_populates="review_as_user", foreign_keys=[account_id])
    counselor = relationship("Account", back_populates="review_as_counselor", foreign_keys=[account_id_counselor])

    def serialize(self, full=True):
        data = {
            'review_counselor_id': self.review_counselor_id,
            'content': self.content,
            'created_at': self.created_at.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'account_id': self.account_id,
            'account_id_counselor': self.account_id_counselor,
        }
        if full:
            data.update({
                'deleted_at': self.deleted_at.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.deleted_at else None
            })
        return data
    
    def __repr__(self):
        return f'<ReviewCounselor {self.review_counselor_id}>'
