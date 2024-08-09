from flask import Blueprint, request
from app.models.report_comment import ReportComment
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_report_comment():
    session = Session()
    try:
        report_comment = session.query(ReportComment).all()
        if not report_comment:
            return api_response(status_code=404, message="No report_comment found", data={})
        
        data = [report_comment.serialize() for report_comment in report_comment]
        return api_response(status_code=200, message="report_comment retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()