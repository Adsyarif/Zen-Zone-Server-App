from app.models.base import  Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, String , func

class ListSchedule(Base):
    __tablename__ = "list_schedule"

    schedule_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    available_from = mapped_column(DateTime(timezone=True), nullable=False)
    available_to = mapped_column(DateTime(timezone=True), nullable=False)
    booked_by_account_id = mapped_column(Integer, ForeignKey('user_details.user_id', ondelete="CASCADE"))
    counselor_id = mapped_column(Integer, ForeignKey('counselor_details.counselor_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    status = mapped_column(String, nullable=True)
    user_details = relationship("UserDetails", back_populates="list_schedule")
    counselor_details = relationship("CounselorDetail", back_populates="list_schedules")

    def serialize(self, full=True):
        data = {
            'schedule_id': self.schedule_id,
            'available_from': self.available_from,
            'available_to': self.available_to,
            'booked_by_account_id': self.booked_by_account_id,
            'counselor_id': self.counselor_id,
            'created_at': self.created_at,
            'status': self.status
        } 
        if full:
            data.update({
                'updated_at': self.updated_at,
                'deleted_at': self.deleted_at
            })
        return data
    
    def __repr__(self):
        return f'<ListSchedule{self.schedule_id}>'