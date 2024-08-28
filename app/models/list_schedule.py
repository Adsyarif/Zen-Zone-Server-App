from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, String, func
from datetime import timezone, timedelta

JAKARTA_TZ = timezone(timedelta(hours=7))
class ListSchedule(Base):
    __tablename__ = "list_schedule"

    schedule_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    available_from = mapped_column(DateTime(timezone=True), nullable=False)
    available_to = mapped_column(DateTime(timezone=True), nullable=False)
    booked_by_account_id = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))
    counselor_id = mapped_column(Integer, ForeignKey('account.account_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    status = mapped_column(String, nullable=True)

    booked_by_account = relationship("Account", back_populates="booked_schedules", foreign_keys=[booked_by_account_id])
    counselor = relationship("Account", back_populates="counselor_schedules", foreign_keys=[counselor_id])

    def serialize(self, full=True):
        data = {
            'schedule_id': self.schedule_id,
            'available_from': self.available_from.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.available_from else None,
            'available_to': self.available_to.astimezone(JAKARTA_TZ).strftime('%Y-%m-%d %H:%M:%S') if self.available_to else None,
            'booked_by_account_id': self.booked_by_account_id,
            'counselor_id': self.counselor_id,
            'created_at': self.created_at,
            'status': self.status,
        } 
        if full:
            data.update({
                'updated_at': self.updated_at,
                'deleted_at': self.deleted_at
            })
        
        return data
    
    def __repr__(self):
        return f'<ListSchedule {self.schedule_id}>'
