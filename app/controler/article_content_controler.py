from flask import request
from app.models.article_content import ArticleContent
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from app.models.articles import Articles

def get_all_article_content():
    session = Session()
    
    try:
        article_contents = session.query(ArticleContent).all()
        data = [article_content.serialize() for article_content in article_contents]
        return api_response(status_code=200, message="article contents retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

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


def create_article_content(article_id):
    session = Session()
    try:
        article = session.query(Articles).filter(Articles.article_id == article_id).first()

        if not article:
            return api_response(status_code=404, message="article id not found", data=[])
        
        data = request.get_json()

        request_fields = ['article_id', 'sub_bab', 'paragraph']
        for field in request_fields:
            if field not in data:
                return api_response(status_code=400, message=f"{field} is required", data={})

        new_article_content = ArticleContent(
            article_id=data['article_id'],
            sub_bab=data['sub_bab'],
            paragraph=data['paragraph']
        )

        session.add(new_article_content)
        session.commit()
        session.refresh(new_article_content)
        return api_response(status_code=201, message="Article created successfully", data=new_article_content.serialize())
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def edit_article_content(article_content_id):
    session = Session()
    try:
        data = request.get_json()

        article_content_to_edit = session.query(ArticleContent).filter(ArticleContent.article_content_id == article_content_id).first()

        if not article_content_to_edit:
            return api_response(status_code=404, message="Article content not found", data={})

        if 'sub_bab' in data:
            article_content_to_edit.sub_bab = data['sub_bab']
        if 'paragraph' in data:
            article_content_to_edit.author = data['paragraph']
        if 'updated_at' in data:
            article_content_to_edit.author = data['updated_at']

        session.commit()
        session.refresh(article_content_to_edit)
        return api_response(status_code=200, message="Article content updated successfully", data=article_content_to_edit.serialize())
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def delete_article_content(article_content_id):
    session = Session()

    try:
        article_content_to_delete = session.query(ArticleContent).filter(ArticleContent.article_content_id == article_content_id).first()

        if not article_content_to_delete:
            return api_response(status_code=404, message="Article content not found", data={})
        
        session.delete(article_content_to_delete)
        session.commit()

        return api_response(status_code=200, message="Article content deleted successfully", data={})
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()