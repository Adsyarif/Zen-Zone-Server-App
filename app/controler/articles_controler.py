from flask import request
from app.models.articles import Articles
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_articles_by_article_id(article_id):
    session = Session()

    try:
        articles = session.query(Articles).filter(Articles.article_id == article_id).all()
        
        if not articles:
            return api_response(status_code=404, message="No articles entries found", data=[])
        data = [article.serialize() for article in articles]
        
        return api_response(status_code=200, message="Articles entries retrieved successfully", data=data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data=[])
    
    finally:
        session.close()

def get_all_articles():
    session = Session()
    
    try:
        articles = session.query(Articles).all()
        data = [article.serialize() for article in articles]
        return api_response(status_code=200, message="articles retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def get_articles_by_tag(tag): 
    session = Session()

    try:
        articles = session.query(Articles).filter(Articles.tag == tag).all()
        
        if not articles:
            return api_response(status_code=404, message="No articles found for the given tag", data=[])
        
        data = [article.serialize() for article in articles]
        return api_response(status_code=200, message="Articles retrieved successfully", data=data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def create_article():
    session = Session()
    try:
        data = request.get_json()

        request_fields = ['title', 'author', 'summary', 'tag']
        for field in request_fields:
            if field not in data:
                return api_response(status_code=400, message=f"{field} is required", data={})

        new_article = Articles(
            title=data['title'],
            author=data['author'],
            summary=data['summary'],
            tag=data['tag']
        )

        session.add(new_article)
        session.commit()
        return api_response(status_code=201, message="Article created successfully", data=new_article.serialize())
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def delete_article(article_id):
    session = Session()

    try:
        article_to_delete = session.query(Articles).filter(Articles.article_id == article_id).first()

        if not article_to_delete:
            return api_response(status_code=404, message="Article not found", data={})
        
        session.delete(article_to_delete)
        session.commit()

        return api_response(status_code=200, message="Article deleted successfully", data={})
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()