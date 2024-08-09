from flask import Blueprint, request, jsonify
from app.models.like import Like
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_like():
    session = Session()
    try:
        like = session.query(Like).all()
        data = [like.serialize() for like in like]
        return api_response(status_code=200, message="like retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()