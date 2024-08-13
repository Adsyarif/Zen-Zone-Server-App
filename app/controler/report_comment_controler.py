from flask import request, jsonify
from app.models.report_comment import ReportComment
from app.models.user_details import UserDetails
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_report_comment():
    session = Session()
    try:
        report_comment = session.query(ReportComment).all()
        if not report_comment:
            return api_response(status_code=404, message="No report_comment found", data={})
        
        data = [report_comment.serialize() for report_comment in report_comment]
        return api_response(status_code=200, message="Get Report Comment successfully", data=data)
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

def do_report_comment(account_id, comment_id):
    session = Session()
    try:
        data = request.json

        report = (
            session.query(ReportComment)
            .join(UserDetails)
            .filter(UserDetails.account_id == account_id, ReportComment.comment_id == comment_id)
            .first()
        )
        if report:
            return jsonify({'message': 'Comment already report by the user'}), 400
        
        if not data.get('report_category_id') and not data.get('report_content'):
            return jsonify({'message': 'Either report_category_id or report_content must be provided'}), 400

        report_comment = ReportComment(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            comment_id=comment_id,
        )

        if data.get('report_category_id'):
            report_comment.report_category_id = data['report_category_id']

        
        if data.get('report_content'):
            report_comment.report_content = data['report_content']

        session.add(report_comment)
        session.commit()

        data = report_comment.serialize()

        return api_response(
            status_code=200,
            message="Report comment created successfully",
            data=report_comment.serialize(full=False)
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