from flask import request
from sqlalchemy import func
from app.models.review_counselor import ReviewCounselor
from app.models.user_details import UserDetails
from app.models.counselor_detail import CounselorDetail
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from sqlalchemy.orm import joinedload
from app.models.account import Account

def get_all_review_counselor():
    session = Session()
    try:
        reviews_counselor = session.query(ReviewCounselor).options(
            joinedload(ReviewCounselor.account).joinedload(Account.user_details),
            joinedload(ReviewCounselor.counselor)
        ).all()

        data = []
        for review in reviews_counselor:
            serialized_review = review.serialize()

            if review.account:
                user_details = review.account.user_details
                counselor_details = review.counselor.counselor_details 

                if isinstance(user_details, list):
                    user_details = user_details[0] if user_details else None
                if isinstance(counselor_details, list):
                    counselor_details = counselor_details[0] if counselor_details else None

                serialized_review.update({
                    'user_first_name': user_details.first_name if user_details else None,
                    'user_last_name': user_details.last_name if user_details else None,
                    'counselor_first_name': counselor_details.first_name if counselor_details else None,
                    'counselor_last_name': counselor_details.last_name if counselor_details else None,
                })
            else:
                serialized_review.update({
                    'user_first_name': None,
                    'user_last_name': None,
                    'counselor_first_name': None,
                    'counselor_last_name': None,
                })

            data.append(serialized_review)

        return api_response(status_code=200, message="Review counselor retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def created_review_counselor(account_id, account_id_counselor):
    session = Session()
    try:
        data = request.get_json()
        content = data.get('content')
        rating = data.get('rating')

        if not content:
            return api_response(status_code=400, message="Missing content", data={})
        
        if not rating:
            return api_response(status_code=400, message="Missing rating", data={})

        user_details = session.query(UserDetails).filter_by(account_id=account_id).first()
        if user_details is None:
            return api_response(status_code=404, message="User not found", data={})

        counselor_details = session.query(CounselorDetail).filter_by(account_id=account_id_counselor).first()
        if counselor_details is None:
            return api_response(status_code=404, message="Counselor not found", data={})

        account_id = user_details.account_id
        account_id_counselor = counselor_details.account_id

        new_review = ReviewCounselor(
            account_id=account_id,
            account_id_counselor=account_id_counselor,
            content=content,
            rating=rating
        )

        session.add(new_review)
        session.commit()

        return api_response(status_code=200, message="Review created successfully", data=new_review.serialize())

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})

    finally:
        session.close()

def soft_delete_review_counselor(review_counselor_id):
    session = Session()
    try:
        account_id = request.json.get('account_id')
        if not account_id:
            return api_response(status_code=400, message="Account ID is required", data={})

        user_details = session.query(UserDetails).filter_by(
            account_id=account_id).first()
        if not user_details:
            return api_response(status_code=404, message="User not found", data={})

        review_counselor = session.query(ReviewCounselor).filter_by(review_counselor_id=review_counselor_id).first()
        if not review_counselor:
            return api_response(status_code=404, message="Post not found", data={})

        if review_counselor.account_id != user_details.account_id:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to delete this post", data={})

        if review_counselor.deleted_at is not None:
            return api_response(status_code=400, message="Review Counselor already deleted", data={})

        review_counselor.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Post soft deleted successfully", data=review_counselor.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

        





