from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
import bcrypt

class Account(Base):
    __tablename__ = "account"

    account_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    role_id = mapped_column(Integer, ForeignKey('role.role_id', ondelete="CASCADE"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    role = relationship("Role", back_populates="account")
    diary = relationship("Diary", back_populates="account")
    user_details = relationship("UserDetails", back_populates="account")

    def serialize(self, full=True):
        data = {
            'account_id': self.account_id,
            'email': self.email,
            'password': self.password,
            'role_id': self.role.serialize() if self.role else None
        }
        if full:
            data.update ({
                'created_at': self.created_at
            })
        return data

    def __repr__(self):
        return f'<Account {self.account_id} - {self.email}>'

    def create_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def confirm_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))