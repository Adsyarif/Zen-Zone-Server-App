from flask import Blueprint, request
from app.models.report_post import ReportPost
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_report_post():
    session = Session()
    try:
        report_post = session.query(ReportPost).all()
        if not report_post:
            return api_response(status_code=404, message="No report_post found", data={})
        
        data = [report_post.serialize() for report_post in report_post]
        return api_response(status_code=200, message="report_post retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()