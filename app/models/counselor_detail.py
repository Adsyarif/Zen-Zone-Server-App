from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, DECIMAL, ForeignKey, DateTime, ARRAY, Text, func

class CounselorDetail(Base):
    __tablename__ = "counselor_details"
    
    counselor_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name = mapped_column(String(255), nullable=False)
    last_name = mapped_column(String(255), nullable=False)
    title = mapped_column(String(255), nullable=False)
    user_name = mapped_column(String(255), nullable=False, unique=True)
    phone_number = mapped_column(String(255), nullable=False, unique=True)
    certification = mapped_column(String(255), nullable=False, unique=True)
    profile_image = mapped_column(String(255), nullable=True)
    price = mapped_column(DECIMAL(10,2), nullable=False)
    alumnus = mapped_column((ARRAY(String)), nullable=False)
    practice_location = mapped_column(Text, nullable=False)
    year_of_experience = mapped_column(Integer, nullable=False)
    practice_license_status = mapped_column(String(255), nullable=False, unique=True)


    gender_id = mapped_column(Integer, ForeignKey('gender.gender_id'))
    account_id = mapped_column(Integer, ForeignKey('account.account_id'))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    gender = relationship("Gender", back_populates="counselor_details")
    account = relationship("Account", back_populates="counselor_details")
    list_schedules = relationship("ListSchedule", back_populates="counselor_details")

    def serialize(self, full=True):
        data = {
            'counselor_id': self.counselor_id, 
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': self.title,
            'user_name': self.user_name,
            'phone_number': self.phone_number,
            'certification': self.certification,
            'price': self.price,
             'alumnus': self.alumnus,
            'practice_location': self.practice_location,
            'year_of_experience': self.year_of_experience,
            'practice_license_status': self.practice_license_status,
            'gender_name':self.gender.name,
            'gender_id': self.gender_id, 
            'account_id': self.account_id  
        }
        if full:
            data.update({
                'created_at': self.created_at,
                'updated_at': self.updated_at,
            })
        return data
    
    def __repr__(self):
        return f'<CounselorDetail {self.counselor_id}>'
