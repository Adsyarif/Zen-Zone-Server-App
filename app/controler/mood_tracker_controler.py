from app.models.mood_tracker import MoodTracker
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_mood_tracker():
    session = Session()
    try:
        mood_tracker = session.query(MoodTracker).all()
        data = [mood_tracker.serialize() for mood_tracker in mood_tracker]
        return api_response(status_code=200, message="mood_tracker retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()