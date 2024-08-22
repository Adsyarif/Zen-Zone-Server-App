from app.models.list_schedule import ListSchedule
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_schedule():
    session = Session()
    try:
        schedule = session.query(ListSchedule).all()
        if not schedule:
            return api_response(status_code=404, message="No roles found", data={})
        
        data = [schedule.serialize() for schedule in schedule]
        return api_response(status_code=200, message="Roles retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()