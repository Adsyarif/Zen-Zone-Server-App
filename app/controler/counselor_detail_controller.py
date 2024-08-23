from flask import request
from sqlalchemy import func
from app.models.counselor_detail import CounselorDetail
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from app.models.account import Account
# from sqlalchemy.orm import joinedload


def get_all_counselor_detail():
    session = Session()
    try:
        counselors = session.query(CounselorDetail).all()
        data = [counselors.serialize() for counselors in counselors]
        return api_response(status_code=200, message="Counselors data retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def get_counselor_detail_by_id(counselor_id, account_id):
    session = Session()
    try:
        get_counselor_id = session.query(CounselorDetail).filter(
            CounselorDetail.counselor_id==counselor_id,
            CounselorDetail.account_id==account_id
        ).first()

        if not get_counselor_id:
            return api_response(status_code=404, message="Counselor detail not found", data={})
        
        serialized_counselor_data = get_counselor_id.serialize()
        return api_response(status_code=200, message="Counselor detail retrieved successfully", data=serialized_counselor_data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        

def create_new_counselor_id(account_id):
    session = Session()
    try:
        data = request.json
         
        required_body_fields = [
             'first_name',
             'last_name',
             'title',
             'user_name',
             'phone_number',
             'certification',
             'gender_id',
             'account_id'
        ]

        for body_field in required_body_fields:
            if body_field not in data:
                return api_response(
                    status_code=400,
                    message=f"{body_field} is required",
                    data={}
                )
        account = session.query(Account).filter(Account.account_id == account_id).first()
        if not account:
            return api_response(
                status_code=404,
                message="Account not found",
                data={}
            )
        
        new_counselor_detail = CounselorDetail(
            account_id=account_id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            title=data["title"],
            user_name=data["user_name"],
            phone_number=data["phone_number"],
            certification=data["certification"],
            gender_id=data["gender_id"]
        )

        session.add(new_counselor_detail)
        session.commit()

        return api_response(
            status_code=200,
            message="New counselor detail created successfully",
            data=new_counselor_detail.serialize(full=False)
        )

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()


def update_counselor_detail_by_id(account_id, counselor_id):
    session = Session()
    try:
        counselor_to_edit = session.query(CounselorDetail).filter(
            CounselorDetail.counselor_id == counselor_id,
            CounselorDetail.account_id == account_id
            ).first()
        if not counselor_to_edit:
            return api_response(status_code=404, message="counselor not found", data={})
        
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        title = request.json.get("title")
        user_name = request.json.get("user_name")
        phone_number = request.json.get("phone_number")
        certification = request.json.get("certification")
        # created_at = request.json.get("created_at")

        counselor_to_edit.first_name = first_name
        counselor_to_edit.last_name = last_name
        counselor_to_edit.title = title
        counselor_to_edit.user_name = user_name
        counselor_to_edit.phone_number = phone_number
        counselor_to_edit.certification = certification
        # counselor_to_edit.created_at= created_at

        session.commit()
        return api_response(status_code=200, message="Counselor data updated successfully", data=counselor_to_edit.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()