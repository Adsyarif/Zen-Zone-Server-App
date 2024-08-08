from app.models import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func

class Mood_status(Base):
    __tablename__ = "mood_status"

    status_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    mood_category_id = mapped_column(Integer, ForeignKey('mood_category.mood_category_id', ondelete="CASCADE"))
    value = mapped_column(String(255), nullable=False)

    mood_category = relationship("Mood_category", back_populates="mood_status")
    diary = relationship("Diary", back_populates="mood_status")

    def serialize(self):
        return {
            'status_id': self.status_id,
            'mood_category_id': self.mood_category_id,
            'value': self.value
        }

    def __repr__(self):
        return f'<MoodCategory{self.id}>'