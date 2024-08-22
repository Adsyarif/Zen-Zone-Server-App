from flask import request
from app.models.article_content import ArticleContent
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_artilce_content_by_article_id(article_id):
    session = Session()
    try:
        article = session.query(ArticleContent).filter(ArticleContent.article_id == article_id).all()
        
        if not article:
            return api_response(status_code=404, message="No article entries found for this account", data=[])
        data = [article.serialize() for article in article]
        
        return api_response(status_code=200, message="Article entries retrieved successfully", data=data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data=[])
    
    finally:
        session.close()