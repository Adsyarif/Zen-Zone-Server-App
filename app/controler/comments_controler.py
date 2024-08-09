from flask import Blueprint, request, jsonify
from app.models.comments import Comments
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_comments():
    session = Session()
    try:
        comments = session.query(Comments).all()
        data = [comments.serialize() for comments in comments]
        return api_response(status_code=200, message="Accounts retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()