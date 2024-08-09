<<<<<<< HEAD
from app.models.base import Base
from sqlalchemy.orm import mapped_column
=======
from app.models import Base
from sqlalchemy.orm import mapped_column, relationship
>>>>>>> 97ca751b837b8574e73705fab36ea04bc850ee8e
from sqlalchemy import Integer, String

class Gender(Base):
    __tablename__ = "gender"

    gender_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)

    user_details = relationship("User_details", back_populates="gender")

    def serialize(self):
        return {
            'gender_id': self.gender_id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Gender {self.gender_id} - {self.name}>'
