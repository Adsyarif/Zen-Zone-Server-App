from flask import  request, jsonify
from app.models.report_post import ReportPost
from app.models.user_details import UserDetails
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_report_post():
    session = Session()
    try:
        report_post = session.query(ReportPost).all()
        if not report_post:
            return api_response(status_code=404, message="No report_post found", data={})
        
        data = [report_post.serialize(False) for report_post in report_post]
        return api_response(status_code=200, message="Get Report Post successfully", data=data)
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

def do_report_post(account_id, post_id):
    session = Session()
    try:
        data = request.json

        report = (
            session.query(ReportPost)
            .join(UserDetails)
            .filter(UserDetails.account_id == account_id, ReportPost.post_id == post_id)
            .first()
        )
        if report:
            return jsonify({'message': 'Post already reported by the user'}), 400
        
        if not data.get('report_category_id') and not data.get('report_content'):
            return jsonify({'message': 'Either report_category_id or report_content must be provided'}), 400

        report_post = ReportPost(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id,
        )

        if data.get('report_category_id'):
            report_post.report_category_id = data['report_category_id']
        
        if data.get('report_content'):
            report_post.report_content = data['report_content']

        session.add(report_post)
        session.commit()

        return api_response(
            status_code=200,
            message="Report Post successfully",
            data=report_post.serialize(full=False)
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