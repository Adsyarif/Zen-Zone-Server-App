<<<<<<< HEAD
from app.models.base import Base
from sqlalchemy.orm import mapped_column
=======
from app.models import Base
from sqlalchemy.orm import mapped_column, relationship
>>>>>>> 97ca751b837b8574e73705fab36ea04bc850ee8e
from sqlalchemy import Integer, String

class Role(Base):
    __tablename__ = "role"

    role_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)

    account = relationship("Account", back_populates="role", lazy='joined')

    def serialize(self):
        return {
            'role_id': self.role_id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Role{self.role_id} - {self.name}>'
