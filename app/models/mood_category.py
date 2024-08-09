from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, func

class MoodCategory(Base):
    __tablename__ = "mood_category"

    mood_category_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255))

    mood_status = relationship("MoodStatus", back_populates="mood_category")

    def serialize(self):
        return {
            'mood_category_id': self.mood_category_id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Mood_category{self.name}>'