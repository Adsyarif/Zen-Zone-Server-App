from app.models import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, ForeignKey


class Gender(Base):
    __tablename__ = "account"

    gender_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            'gender_id': self.gender_id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Gender{self.id} - {self.name}>'
