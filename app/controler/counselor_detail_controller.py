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
        account = session.query(Account).filter(Account.account_id).first()
        if not account:
            return api_response(
                status_code=404,
                message="Account not found",
                data={}
            )
        
        new_counselor_detail = CounselorDetail(
            account_id=account_id,
            first_name=["first_name"],
            last_name=["last_name"],
            title=["title"],
            user_name=["user_name"],
            phone_number=["phone_number"],
            certification=["certification"],
            gender_id=["gender_id"]
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

