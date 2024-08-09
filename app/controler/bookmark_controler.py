from flask import Blueprint, request, jsonify
from app.models.bookmarks import Bookmarks
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_bookmarks():
    session = Session()
    try:
        bookmarks = session.query(Bookmarks).all()
        data = [bookmarks.serialize() for bookmarks in bookmarks]
        return api_response(status_code=200, message="bookmarks retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()