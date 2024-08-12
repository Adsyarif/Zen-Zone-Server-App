from flask import Blueprint, request, jsonify
from app.models.diary import Diary
# from app.models.mood_status import MoodStatus
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_diary():
    session = Session()
    try:
        diary = session.query(Diary).all()
        data = [diary.serialize() for diary in diary]
        return api_response(status_code=200, message="diary retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
