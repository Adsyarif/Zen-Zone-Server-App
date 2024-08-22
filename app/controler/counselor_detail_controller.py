from flask import request
from sqlalchemy import func
from app.models.counselor_detail import CounselorDetail
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
# from app.models.account import Account
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

# def get_counselor_detail_by_id(account_id):
#     session = Session()
#     try:
#         account = session.query(Account).options(joinedload(Account.counselor_details)).filter(Account.account_id == account_id).first()
#         if not account:
#             return api_response(status_code=404, message="Counselor detail by id not found", data={})
        
#         account_data = {

#         }

