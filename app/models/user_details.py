from app.models.base import Base
from app.models.gender import Gender 
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

class UserDetails(Base):
    __tablename__ = "user_details"

    user_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))
    first_name = mapped_column(String(255), nullable=False)
    last_name = mapped_column(String(255), nullable=False)
    user_name = mapped_column(String(255), nullable=False, unique=True)
    phone_number = mapped_column(String(255), nullable=False, unique=True)
    profile_image = mapped_column(String(255), nullable=True)  # Ubah nullable=True jika profile_image tidak wajib
    gender_id = mapped_column(Integer, ForeignKey('gender.gender_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    gender = relationship("Gender", back_populates="user_details", lazy='joined')    
    account = relationship("Account", back_populates="user_details", lazy='joined')

    def serialize(self, full=True):
        data = {
            'user_id': self.user_id,
            'account_id': self.account_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_name': self.user_name,
            'phone_number': self.phone_number,
            'gender_id': self.gender_id
        }
        if full:
            data.update({
                'created_at': self.created_at,
                'updated_at': self.updated_at,
            })
        return data

    def __repr__(self):
        return f'<UserDetails {self.user_id}>'
