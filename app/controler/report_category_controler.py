from flask import Blueprint, request
from app.models.report_category import ReportCategory
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_report_category():
    session = Session()
    try:
        report_category = session.query(ReportCategory).all()
        if not report_category:
            return api_response(status_code=404, message="No report_category found", data={})
        
        data = [report_category.serialize() for report_category in report_category]
        return api_response(status_code=200, message="report_category retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()