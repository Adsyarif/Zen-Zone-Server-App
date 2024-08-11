from flask import Blueprint, request, jsonify
from app.models.like import Like
from app.models.posts import Posts
from app.models.user_details import UserDetails
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_like():
    session = Session()
    try:
        like = session.query(Like).all()
        data = [like.serialize() for like in like]
        return api_response(status_code=200, message="like retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def do_like_post(account_id, post_id):
    session = Session()
    try:
        # data = request.json
        
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not user_query:
            return jsonify({'message': 'User invalid'}), 400
        
        post_query = session.query(Posts).filter(Posts.post_id == post_id)
        if not post_query:
            return jsonify({'message': 'No related post found'}), 400
        
        like_query = session.query(Like).join(UserDetails).filter(UserDetails.account_id == account_id, Like.post_id == post_id).first()
        if like_query:
            return jsonify({'message': 'Post already liked by the user'}), 400
        
        add_like = Like(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id
        )
        
        # if data.get('')
        
        session.add(add_like)
        session.commit()
        
        # data = add_like.serialize()
        
        return api_response(
            status_code=200,
            message="Post successfully liked",
            data=add_like.serialize(full=False)
        )
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return api_response(
            status_code=500,
            message=f"server error: {str(e)}",
            data={}
        )
    finally:
        session.close()
        
def remove_like(account_id, post_id):
    session = Session()
    
    try:
        likes_to_delete = session.query(Like).join(UserDetails).filter(UserDetails.account_id == account_id, Like.post_id == post_id).first()
        session.delete(likes_to_delete)
        session.commit()
        
        return api_response(
            status_code=200,
            message="Like successfully removed",
            data={}
        )
        
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return api_response(
            status_code=500,
            message=f"server error: {str(e)}",
            data={}
        )
    
    finally:
        session.close()
    
def get_like_by_account_id(account_id):
    session = Session()
    
    try:
        like_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not like_query:
            return jsonify({'message': 'User Invalid'}), 400
        data = [like_query.serialize() for like_query in like_query]
        return api_response(status_code=200, message="like retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
