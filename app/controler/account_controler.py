from flask import Blueprint, request, jsonify
from app.models.account import Account
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

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