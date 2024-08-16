from app.models.role import Role
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_roles():
    session = Session()
    try:
        roles = session.query(Role).all()
        if not roles:
            return api_response(status_code=404, message="No roles found", data={})
        
        data = [role.serialize() for role in roles]
        return api_response(status_code=200, message="Roles retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()