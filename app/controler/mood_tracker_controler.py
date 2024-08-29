from app.models.mood_tracker import MoodTracker
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_mood_tracker_by_account_id(account_id):
    session = Session()
    try:
        mood_trackers = session.query(MoodTracker).join(MoodTracker.diary).filter(MoodTracker.diary.has(account_id=account_id)).all()

        data = [{
            'mood_tracker_id': mt.mood_tracker_id,
            'diary_id': mt.diary.diary_id,
            'account_id': mt.diary.account_id,
            'status_id': mt.diary.status_id
        } for mt in mood_trackers]
        
        return api_response(status_code=200, message="MoodTracker retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()