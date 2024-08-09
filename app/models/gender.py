from app.models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String

class Gender(Base):
    __tablename__ = "gender"

    gender_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            'gender_id': self.gender_id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Gender{self.gender_id} - {self.name}>'
