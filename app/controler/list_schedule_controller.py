from app.models.list_schedule import ListSchedule
from app.connector.sql_connector import Session
from app.models.user_details import UserDetails
from app.models.counselor_detail import CounselorDetail
from app.utils.api_response import api_response
from flask import  request, jsonify


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
        
def get_schedule_by_counselor_id(counselor_id):
    session = Session()
    try:
        schedule_query = session.query(ListSchedule).filter(ListSchedule.counselor_id == counselor_id).all()
        
        if not schedule_query:
            return api_response(status_code=400, message="No schedule found", data={})
        data = [schedule_query.serialize() for schedule_query in schedule_query]
        
        return api_response(status_code=200, message="List schedule by counselor_id retrieved successfully", data=data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def post_schedule_by_counselor_id(counselor_id):
    session = Session()
    try:
        data = request.get_json()
        available_from = data.get('available_from')
        available_to = data.get('available_to')
        created_at = data.get('created_at')
        
        
        if not available_from:
            return api_response(status_code=400, message="Missing required schedule", data={})
        if not available_to:
            return api_response(status_code=400, message="Missing required schedule", data={})
        
        counselor_query = session.query(CounselorDetail).filter(CounselorDetail.counselor_id == counselor_id).first()
        if not counselor_query:
            return api_response(status_code=404, message="No such counselor found", data={})
        
        new_schedule = ListSchedule(
            counselor_id=counselor_id,
            available_from=available_from,
            available_to=available_to,
            created_at=created_at
        )
        
        session.add(new_schedule)
        session.commit()
        return api_response(status_code=201, message="Schedule successfully reserved", data=new_schedule.serialize(full=False))
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def put_user_booked_by_account_id(account_id, schedule_id):
    session = Session()
    try:
        data = request.get_json()
        updated_at = data.get('updated_at')
        
        schedule_query = session.query(ListSchedule).filter(ListSchedule.schedule_id == schedule_id)
        if not schedule_query:
            return api_response(status_code=400, message="No schedule found", data={})
        
        account_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not account_query:
            return api_response(status_code=400, message="No such account found", data={})
        
        listed_schedule_query = session.query(ListSchedule).join(UserDetails).filter(UserDetails.account_id == account_id, ListSchedule.schedule_id == schedule_id).first()
        if not listed_schedule_query:
            return api_response(status_code=403, message="schedule booking not allowed", data={})
        
        listed_schedule_query.booked_by_account_id = account_id
        listed_schedule_query.updated_at = updated_at
        
        session.commit()
        return api_response(status_code=200, message="Schedule booked successfully", data=listed_schedule_query.serialize(full=False))
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def put_user_reschedule_by_schedule_id(account_id, schedule_id):
    session = Session()
    try:
        data = request.get_json()
        updated_at = data.get('updated_at')
        
        
        schedule_query = session.query(ListSchedule).filter(ListSchedule.schedule_id == schedule_id)
        if not schedule_query:
            return api_response(status_code=400, message="No schedule found", data={})
        
        account_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not account_query:
            return api_response(status_code=400, message="No such account found", data={})
        
        session_reschedule = session.query(ListSchedule).join(CounselorDetail).filter(
            ListSchedule.schedule_id == schedule_id,
            CounselorDetail.account_id == account_id
        ).first()
        if not session_reschedule:
            return api_response(status_code=403, message="Schedule edit not authorized", data={})
        
        session_reschedule.booked_by_account_id = account_id
        session_reschedule.updated_at = updated_at
        
        session.commit()
        return api_response(status_code=200, message="Session reschedule successfully", data=session_reschedule.serialize(full=True))
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def put_cancel_by_account_id(account_id, schedule_id):
    session = Session()
    try:
        # data = request.get_json()
        # updated_at = data.get('updated_at')
        
        schedule_query = session.query(ListSchedule).filter(ListSchedule.schedule_id == schedule_id)
        if not schedule_query:
            return api_response(status_code=400, message="No schedule found", data={})
        
        account_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not account_query:
            return api_response(status_code=400, message="No such account found", data={})
        
        canceled_schedule_query = session.query(ListSchedule).join(UserDetails).filter(UserDetails.account_id == account_id, ListSchedule.schedule_id == schedule_id).first()
        if not canceled_schedule_query:
            return api_response(status_code=403, message="Unable to cancel schedule", data={})
        
        cancel_schedule = canceled_schedule_query.booked_by_account_id.delete()
        cancel_schedule.execute()
        
        session.commit()
        return api_response(status_code=200, message="Schedule Canceled Successfully", data={})
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def delete_schedule_by_counselor_id(counselor_id):
    session = Session()
    try:
        counselor_query = session.query(ListSchedule).filter(ListSchedule.counselor_id == counselor_id).first()
        if not counselor_query:
            return api_response(status_code=400, message="No such counselor found", data={})
        
        session.delete(counselor_query)
        session.commit()
        
        return api_response(status_code=200, message="Schedule successfully deleted", data={})
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
