from app.models import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Integer, String


class UserDetails(Base):
    __tablename__ = "user_details"

    user_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = relationship("Account", back_populates="user_details")
    first_name = mapped_column(String(255), nullable=False)
    last_name = mapped_column(String(255), nullable=False)
    user_name = mapped_column(String(255), nullable=False, unique=True)
    phone_number = mapped_column(String(255), nullable=False, unique=True)
    updated_at = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    gender_id = relationship("Gender", back_populates="user_details")

    # Termporal profile image
    profile_image = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'account_id': self.account_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_name': self.user_name,
            'user_id': self.user_id,
            'phone_number': self.phone_number,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
            'gender_id': self.gender_id
        }

    def __repr__(self):
        return f'<account{self.id} - {self.email}>'
