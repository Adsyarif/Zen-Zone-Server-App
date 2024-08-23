from app.models.list_schedule import ListSchedule
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_list_schedules():
    session = Session()
    try:
        list_schedule = session.query(ListSchedule).all()
        if not list_schedule:
            return api_response(status_code=404, message="No list schedule found", data={})
        
        data = [list_schedule.serialize() for list_schedule in list_schedule]
        return api_response(status_code=200, message="List schedule retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()