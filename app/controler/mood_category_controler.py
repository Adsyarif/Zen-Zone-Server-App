from app.models.mood_category import MoodCategory
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_mood_category():
    session = Session()
    try:
        mood_category = session.query(MoodCategory).all()
        data = [mood_category.serialize() for mood_category in mood_category]
        return api_response(status_code=200, message="mood_category retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()