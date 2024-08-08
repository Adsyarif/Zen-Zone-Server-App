from app.models import Base
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
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now(), ondelete=func.now())

    account = relationship("Account", back_populates="diary")
    mood_status = relationship("Mood_status", back_populates="diary")
    mood_tracker = relationship("", back_populates="diary") 