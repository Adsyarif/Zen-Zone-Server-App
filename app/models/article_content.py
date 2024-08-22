from app.models.base import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class ArticleContent(Base):
    __tablename__ = "article_content"

    article_content_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id = mapped_column(Integer, ForeignKey('articles.article_id', ondelete="CASCADE"), nullable=False)
    sub_bab = mapped_column(String, nullable=False)
    paragraph = mapped_column(String, nullable=False)

    articles = relationship("Articles", back_populates="article_content")

    
    def serialize(self):
        return {
            'article_content_id': self.article_content_id,
            'article_id': self.article_id,
            'sub_bab': self.sub_bab,
            'paragraph': self.paragraph
        }
    
    def __repr__(self):
        return f'<ArticleContent {self.article_content_id}>'