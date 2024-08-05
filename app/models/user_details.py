from app.models import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, ForeignKey


class Account(Base):
    __tablename__ = "account"

    account_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    role_at = mapped_column(Integer, ForeignKey())
