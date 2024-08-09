from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey

class MoodTracker(Base):
    __tablename__ = "mood_tracker"

    mood_tracker_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    diary_id = mapped_column(Integer, ForeignKey('diary.diary_id', ondelete="CASCADE"))

    diary = relationship("Diary", back_populates="mood_tracker")

    def serialize(self):
        return {
            'mood_tracker_id': self.mood_tracker_id,
            'diary_id': self.diary_id
        }
    
    def __repr__(self):
        return f'<Mood_tracker{self.mood_tracker_id}>'