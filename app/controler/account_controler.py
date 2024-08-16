from flask import request, jsonify
from pydantic import ValidationError
from app.models.account import Account
from app.connector.sql_connector import Session
from app.models.user_details import UserDetails
from app.utils.api_response import api_response
from app.validations.account_validation import CreateAccount, LoginAccount
from flask_jwt_extended import create_access_token

def create_account():
    try:
        account_data = CreateAccount(**request.json)
    except ValidationError as e:
        return jsonify(f"Validation error occured: {e}")

    email = account_data.email
    password = account_data.password
    role_id = account_data.role_id

    session = Session()
    existing_account = session.query(Account).filter(Account.email == email).first()
    if existing_account:
        session.close()
        return jsonify(f"Email'{email}' already exists. create with another data")
    
    new_account = Account(
        email = email,
        password = password,
        role_id = role_id
    )
    new_account.create_password(password)

    try:
        session.add(new_account)
        session.commit()
        session.refresh(new_account)
    except Exception as e:
        session.rollback()
        return api_response(
            status_code = 500, 
            message = f"create account failed: {e}", 
            data = {}
        )
    finally:
        session.close()
    return api_response(
        status_code = 201,
        message = "create account success",
        data = {}
    )

def get_user_profile_status(account_id):
    session = Session()
    user_details = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()
    return user_details is not None

def login_account():
    try:
        login_data = LoginAccount(**request.json)
    except ValidationError as e:
        return jsonify(f"Validation error occured: {e}")

    email = login_data.email
    password = login_data.password

    session = Session()
    session.begin()
    try:
        account = session.query(Account).filter(Account.email == email).first()

        if account == None:
            return api_response(
                status_code = 404,
                message = "account not found, please signup first",
                data = {}
            )
        if not account.confirm_password(password):
            return api_response(
                status_code = 404,
                message = "password incorrect, please check again",
                data = {}
            )
        profile_incomplete = not get_user_profile_status(account.account_id)
        access_token = create_access_token(identity = account.account_id)

        return api_response(
            status_code=200,
            message="Login success",
            data={
                "account": account.serialize(),
                "access_token": access_token,
                "profile_incomplete": profile_incomplete
            }
        )
    except Exception as e:
        session.rollback()
        return api_response(
            status_code = 500, 
            message = f"Login failed: {e}", 
            data = {}
        )
    finally:
        session.close()

def get_all_accounts():
    session = Session()
    try:
        accounts = session.query(Account).all()
        data = [account.serialize() for account in accounts]
        return api_response(
            status_code = 200, 
            message = "Accounts retrieved successfully", 
            data = data
        )
    except Exception as e:
        return api_response(
            status_code = 500, 
            message = f"Server error: {e}", 
            data = {}
        )
    finally:
        session.close()