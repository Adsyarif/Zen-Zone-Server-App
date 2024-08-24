from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, func


class Articles(Base):
    __tablename__ = "articles"

    article_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String, nullable=False)
    author = mapped_column(String, nullable=False)
    summary = mapped_column(String, nullable=False)
    tag = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True)

    article_content = relationship("ArticleContent", back_populates="articles", cascade="all, delete-orphan")

    def serialize(self):
        return {
            'article_id': self.article_id,
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'tag': self.tag,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
    
    def __repr__(self):
        return f'<Article {self.article_id}>'