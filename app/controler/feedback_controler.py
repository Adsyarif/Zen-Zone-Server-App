from flask import request
from app.models.feedback import Feedback
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from sqlalchemy import func


def get_feedback_by_account_id(account_id):
    session = Session()
    try:
        feedback = session.query(Feedback).filter(Feedback.account_id == account_id).all()
        
        if not feedback:
            return api_response(status_code=404, message="No Feedback entries found for this account", data=[])
        data = [feedback.serialize() for feedback in feedback]
        
        return api_response(status_code=200, message="Feedback entries retrieved successfully", data=data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data=[])
    
    finally:
        session.close()


def get_all_feedback():
    session = Session()
    try:
        feedback = session.query(Feedback).all()
        data = [feedback.serialize() for feedback in feedback]
        return api_response(status_code=200, message="Feedback retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def get_feedback_by_id(account_id, feedback_id): 
    session = Session()
    try:
        get_feedback_entry = session.query(Feedback).filter(
            Feedback.feedback_id==feedback_id, 
            Feedback.account_id==account_id
            ).first()
        
        if not get_feedback_entry:
            return api_response(status_code=404, message="Feedback entry not found", data={})
        
        serialized_feedback_entry = get_feedback_entry.serialize()
        return api_response(status_code=200, message="Feedback entry retrieved successfully", data=serialized_feedback_entry)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def create_feedback_entry(account_id):
    session = Session()
    try:
        username = request.json.get("username")  
        description = request.json.get("description")
        rating = request.json.get("rating")
        created_at = request.json.get("created_at")

        if not username:
            return api_response(status_code=400, message="Username content is required", data={})
        if not description:
            return api_response(status_code=400, message="Description is required", data={})
        if not rating:
            return api_response(status_code=400, message="Rating is required", data={})

        new_feedback_entry = Feedback(
            account_id=account_id,
            username=username, 
            description=description,
            rating=rating,
            created_at=created_at,
        )

        session.add(new_feedback_entry)
        session.commit()
        return api_response(status_code=201, message="Feedback created successfully", data=new_feedback_entry.serialize(full=False))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()




def edit_feedback_by_id(account_id, feedback_id):
    session = Session()
    try:

        description = request.json.get("description")
        created_at = request.json.get("created_at")

        # if not content:
        #     return api_response(status_code=400, message="Diary content is required", data={})
        # if not mood_status_id:
        #     return api_response(status_code=400, message="Mood status ID is required", data={})

        feedback_entry_to_edit = session.query(Feedback).filter(
            Feedback.account_id == account_id,
            Feedback.feedback_id_id == feedback_id,
            ).first()
        if not feedback_entry_to_edit:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to edit this feedback entry", data={})

        feedback_entry_to_edit.description = description
        feedback_entry_to_edit.created_at = created_at
        
        session.commit()
        return api_response(status_code=200, message="Feedback updated successfully", data=feedback_entry_to_edit.serialize(full=True))
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def soft_delete_feedback_entry_by_id(feedback_id):
    session = Session()
    try:
        
        feedback_entry_to_delete = session.query(Feedback).filter(
            Feedback.feedback_id==feedback_id,
        ).first()
        
        if not feedback_entry_to_delete:
            return api_response(status_code=404, message="Feedback entry not found", data={})

        
        feedback_entry_to_delete.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Feedback soft deleted successfully", data=feedback_entry_to_delete.serialize(full=True))
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

# def share_diary(account_id, feedback_id):
#     session = Session()
#     try:
#         share = request.json.get("share")

#         if share is None:
#             return api_response(status_code=400, message="The 'share' field is required", data={})

#         diary_entry = session.query(Diary).filter(
#             Diary.account_id == account_id,
#             Diary.diary_id == diary_id
#         ).first()

#         if not diary_entry:
#             return api_response(status_code=403, message="Unauthorized: You are not allowed to edit this diary entry", data={})

#         diary_entry.share = share
#         session.commit()

#         return api_response(status_code=200, message="Diary updated successfully", data=diary_entry.serialize(full=False))

#     except Exception as e:
#         session.rollback()
#         return api_response(status_code=500, message=f"Server error: {e}", data={})
#     finally:
#         session.close()
