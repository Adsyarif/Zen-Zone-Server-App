from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models.account import Account
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from app.validations.account_validation import CreateAccount

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
        return jsonify(f"Email'{email}' already exists. create with another data")
    
    new_account = Account(
        email = email,
        password = password,
        role_id = role_id
    )
    new_account.create_password(password)

    session.begin()
    try:
        session.add(new_account)
        session.commit()
    except Exception as e:
        session.rollback()
        return api_response(status_code = 500, message = f"create account failed: {e}", data = {})
    finally:
        session.close()
    return api_response(
        status_code = 201,
        message = "create account success",
        data = {}
    )

def get_all_accounts():
    session = Session()
    try:
        accounts = session.query(Account).all()
        data = [account.serialize() for account in accounts]
        return api_response(status_code=200, message="Accounts retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()