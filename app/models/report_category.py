from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

class Report_category(Base):
    __tablename__ = "report_category"

    report_category_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    value = mapped_column(String(255))
    
    report_post = relationship("Report_post", back_populates="report_category")
    report_comment = relationship("Report_comment", back_populates="report_category")

    def serialize(self):
        return {
            'report_category_id': self.report_category_id,
            'value': self.value
        }
    
    def __repr__(self):
        return f'<Report_category {self.report_category_id}>'