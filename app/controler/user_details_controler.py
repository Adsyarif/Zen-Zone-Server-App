from flask import request
from sqlalchemy.orm import joinedload
from app.models.user_details import UserDetails
from app.models.account import Account
from app.connector.sql_connector import Session
from app.utils.api_response import api_response


def get_user_details_id(account_id):
    session = Session()

    try:
        account = session.query(Account).options(joinedload(Account.user_details)).filter(Account.account_id == account_id).first()
        if not account:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )
        
        account_data = {
            "email": account.email
        }

        user_details_data = [
            {
                "first_name": user_details.first_name,
                "last_name": user_details.last_name,
                "user_name": user_details.user_name,
                "phone_number": user_details.phone_number,
                "profile_image": user_details.profile_image,
                "gender_name": user_details.gender.name
            }
            for user_details in account.user_details
        ]
        
        return api_response(
            status_code=200,
            message="User and About User data retrieved successfully",
            data={
                "account": account_data,
                "user_details": user_details_data
            }
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()


def get_user_details():
    session = Session()
    try:
        user_details_list = session.query(UserDetails).all()

        if not user_details_list:
            return api_response(
                status_code=404,
                message="No user details found",
                data={}
            )
        
        user_details_data = [
            {
                "first_name": user_details.first_name,
                "last_name": user_details.last_name,
                "user_name": user_details.user_name,
                "phone_number": user_details.phone_number,
                "profile_image": user_details.profile_image,
                "gender_name": user_details.gender.name
            }
            for user_details in user_details_list
        ]
        
        return api_response(
            status_code=200,
            message="User details retrieved successfully",
            data=user_details_data
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()

def create_user_details(account_id):
    session = Session()
    try:
        data = request.json

        required_fields = ['first_name', 'last_name', 'user_name', 'phone_number', 'gender_id']
        for field in required_fields:
            if field not in data:
                return api_response(
                    status_code=400,
                    message=f"{field} is required",
                    data={}
                )
        account = session.query(Account).filter(Account.account_id == account_id).first()
        if not account:
            return api_response(
                status_code=404,
                message="Account not found",
                data={}
            )
        
        new_user_details = UserDetails(
            account_id=account_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_name=data['user_name'],
            phone_number=data['phone_number'],
            gender_id=data['gender_id'],
            
        )

        session.add(new_user_details)
        session.commit()

        return api_response(
            status_code=200,
            message="UserDetails created successfully",
            data=new_user_details.serialize(full=False)
        )
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()

def edit_user_details(account_id):
    session = Session()
    
    try:
        data = request.json
     
        user_details = session.query(UserDetails).join(UserDetails.account).filter(UserDetails.account_id == account_id).first()
        
        if not user_details:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )

        user_details.first_name = data.get('first_name', user_details.first_name)
        user_details.last_name = data.get('last_name', user_details.last_name)
        user_details.user_name = data.get('user_name', user_details.user_name)
        user_details.phone_number = data.get('phone_number', user_details.phone_number)
        user_details.gender_id = data.get('gender_id', user_details.gender_id)

        session.commit()

        return api_response(
            status_code=200,
            message="UserDetails updated successfully",
            data=user_details.serialize(full=False)
        )
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()

    