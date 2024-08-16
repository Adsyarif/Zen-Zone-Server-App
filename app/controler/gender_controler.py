from app.models.gender import Gender
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_genders():
    session = Session()
    try:
        genders = session.query(Gender).all()
        data = [gender.serialize() for gender in genders]
        return api_response(status_code=200, message="Genders retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()