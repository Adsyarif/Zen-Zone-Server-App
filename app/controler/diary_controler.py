from flask import request
from app.models.diary import Diary
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from sqlalchemy import func


def get_diary_by_account_id(account_id):
    session = Session()
    try:
        diary = session.query(Diary).filter(Diary.account_id == account_id).all()
        
        if not diary:
            return api_response(status_code=404, message="No diary entries found for this account", data=[])
        data = [diary.serialize() for diary in diary]
        
        return api_response(status_code=200, message="Diary entries retrieved successfully", data=data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data=[])
    
    finally:
        session.close()


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
        created_at = request.json.get("created_at")

        if not content:
            return api_response(status_code=400, message="Diary content is required", data={})
        if not mood_status_id:
            return api_response(status_code=400, message="Mood Status ID is required", data={})

        new_diary_entry = Diary(
            account_id=account_id,
            mood_status_id=mood_status_id,
            content=content,
            created_at=created_at,
        )

        session.add(new_diary_entry)
        session.commit()
        return api_response(status_code=201, message="Diary created successfully", data=new_diary_entry.serialize(full=False))

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
        created_at = request.json.get("created_at")

        if not content:
            return api_response(status_code=400, message="Diary content is required", data={})
        if not mood_status_id:
            return api_response(status_code=400, message="Mood status ID is required", data={})

        diary_entry_to_edit = session.query(Diary).filter(
            Diary.account_id == account_id,
            Diary.diary_id == diary_id,
            ).first()
        if not diary_entry_to_edit:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to edit this diary entry", data={})

        diary_entry_to_edit.content = content
        diary_entry_to_edit.mood_status_id = mood_status_id
        diary_entry_to_edit.created_at = created_at
        
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
        
        diary_entry_to_delete = session.query(Diary).filter(
            Diary.diary_id==diary_id,
            Diary.account_id==account_id
        ).first()
        
        if not diary_entry_to_delete:
            return api_response(status_code=404, message="Diary entry not found", data={})

        
        diary_entry_to_delete.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Diary soft deleted successfully", data=diary_entry_to_delete.serialize(full=True))
    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
