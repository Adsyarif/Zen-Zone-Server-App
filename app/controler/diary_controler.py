from flask import Blueprint, request, jsonify
from app.models.diary import Diary
# from app.models.mood_status import MoodStatus
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from sqlalchemy import func
from app.models.account import Account


# def get_all_diary():
#     session = Session()
#     try:
#         diary = session.query(Diary).all()
#         data = [diary.serialize(full=True) for diary in diary]
#         return api_response(status_code=200, message="Diary retrieved successfully", data=data)
#     except Exception as e:
#         return api_response(status_code=500, message=f"Server error: {e}", data={})
#     finally:
#         session.close()

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


def get_diary_by_id(account_id, diary_id): 
    session = Session()
    try:
        get_diary_entry = session.query(Diary).filter(
            Diary.diary_id==diary_id, 
            Diary.account_id==account_id
            ).first()
        
        if not get_diary_entry:
            return api_response(status_code=404, message="Diary entry not found", data={})
        
        serialized_diary_entry = get_diary_entry.serialize()
        return api_response(status_code=200, message="Diary entry retrieved successfully", data=serialized_diary_entry)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def create_diary_entry(account_id):
    session = Session()
    try:
        content = request.json.get("content")
        mood_status_id = request.json.get("mood_status_id")

        if not content:
            return api_response(status_code=400, message="Diary content is required", data={})
        if not mood_status_id:
            return api_response(status_code=400, message="Mood Status ID is required", data={})

        new_diary_entry = Diary(
            account_id=account_id,
            mood_status_id=mood_status_id,
            content=content
        )

        session.add(new_diary_entry)
        session.commit()
        return api_response(status_code=201, message="Diary created successfully", data=new_diary_entry.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()



def edit_diary_by_id(account_id, diary_id):
    session = Session()
    try:
        content = request.json.get("content")
        mood_status_id = request.json.get("mood_status_id")
        # account_id = request.json.get("account_id")

        if not content:
            return api_response(status_code=400, message="Diary content is required", data={})
        if not mood_status_id:
            return api_response(status_code=400, message="Mood status ID is required", data={})
        # if not account_id:
        #     return api_response(status_code=400, message="Account ID is required", data={})

        diary_entry_to_edit = session.query(Diary).filter(
            Diary.account_id == account_id,
            Diary.diary_id == diary_id
            ).first()
        if not diary_entry_to_edit:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to edit this diary entry", data={})

        diary_entry_to_edit.content = content
        diary_entry_to_edit.mood_status_id = mood_status_id
        
        session.commit()
        return api_response(status_code=200, message="Diary updated successfully", data=diary_entry_to_edit.serialize(full=True))
    
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def soft_delete_diary_entry_by_id(account_id, diary_id):
    session = Session()
    try:
        request_data = request.json
        mood_status_id = request_data.get("mood_status_id")
        content = request_data.get("content")

        if not mood_status_id:
            return api_response(status_code=400, message="Mood status ID is required", data={})
        
        if not content:
            return api_response(status_code=400, message="Diary content is required", data={})
        
        diary_entry_to_delete = session.query(Diary).filter(
            Diary.diary_id==diary_id,
            Diary.account_id==account_id
        ).first()
        
        if not diary_entry_to_delete:
            return api_response(status_code=404, message="Diary entry not found", data={})

        diary_entry_to_delete.content = content
        diary_entry_to_delete.mood_status_id = mood_status_id
        
        if diary_entry_to_delete.deleted_at is not None:
            return api_response(status_code=400, message="Diary entry is deleted and cannot be updated", data={})
        
        diary_entry_to_delete.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Diary soft deleted successfully", data=diary_entry_to_delete.serialize(full=True))
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
