from flask import  jsonify
from app.models.mood_status import MoodStatus
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_mood_status():
    session = Session()
    try:
        mood_status = session.query(MoodStatus).all()
        data = [mood_status.serialize() for mood_status in mood_status]
        return api_response(status_code=200, message="mood_status retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def get_mood_status_by_status_id(status_id):
    session = Session()
    try:
        mood_status = session.query(MoodStatus).filter(MoodStatus.status_id == status_id).first()
        
        if not mood_status:
            return jsonify({'message': 'Mood not listed'}), 400
        

        data = mood_status.serialize()  

        return api_response(status_code=200, message="Specified mood status retrieved successfully", data=data)
    
    except Exception as e:
        print(f"General error: {e}")
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def get_mood_status_by_status_id(status_id):
    session = Session()
    try:
        mood_status = session.query(MoodStatus).filter(MoodStatus.status_id == status_id).first()
        
        if not mood_status:
            return jsonify({'message': 'Mood not listed'}), 400

        data = mood_status.serialize()  

        return api_response(status_code=200, message="Specified mood status retrieved successfully", data=data)

    except Exception as e:
        print(f"General error: {e}")
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()