from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func

class Diary(Base):
    __tablename__ = "diary"

    diary_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))
    mood_status_id = mapped_column(Integer, ForeignKey('mood_status.status_id', ondelete="CASCADE"))
    content = mapped_column(String)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="diary")
    mood_status = relationship("MoodStatus", back_populates="diary")
    mood_tracker = relationship("MoodTracker", back_populates="diary")

    def serialize(self, full=True):
        data = {
            'diary_id': self.diary_id,
            'account_id': self.account_id, 
            'mood_status_id': self.mood_status.serialize() if self.mood_status else None,
            'content': self.content,
            'value': self.mood_status.value,
            'created_at': self.created_at,
        }
        if full:
            data.update ({
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'deleted_at': self.deleted_at
            })
        return data
    
    def __repr__(self):
        return f'<Diary{self.diary_id}>'