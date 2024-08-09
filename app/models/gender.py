from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

class Gender(Base):
    __tablename__ = "gender"

    gender_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)

    user_details = relationship("User_details", back_populates="gender")

    user_details = relationship("UserDetails", back_populates="gender")

    def serialize(self):
        return {
            'gender_id': self.gender_id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Gender {self.gender_id} - {self.name}>'
