from flask import Blueprint, request
from app.models.posts import Posts
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_post():
    session = Session()
    try:
        post = session.query(Posts).all()
        if not post:
            return api_response(status_code=404, message="No post found", data={})
        
        data = [post.serialize() for post in post]
        return api_response(status_code=200, message="post retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()