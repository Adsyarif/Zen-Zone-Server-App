from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

class Role(Base):
    __tablename__ = "role"

    role_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    value = mapped_column(String(255), nullable=False)

    account = relationship("Account", back_populates="role")


    def serialize(self):
        return {
            'role_id': self.role_id,
            'value': self.value
        }

    def __repr__(self):
        return f'<Role{self.role_id} - {self.value}>'
