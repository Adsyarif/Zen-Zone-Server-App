from flask import Blueprint, request, jsonify
from app.models.bookmarks import Bookmarks
from app.models.posts import Posts
from app.models.user_details import UserDetails
from app.connector.sql_connector import Session
from app.utils.api_response import api_response

def get_all_bookmarks():
    session = Session()
    try:
        bookmarks = session.query(Bookmarks).all()
        data = [bookmarks.serialize() for bookmarks in bookmarks]
        return api_response(status_code=200, message="bookmarks retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
        
def do_bookmark_post(account_id, post_id):
    session = Session()
    try:
        # data = request.json
        
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not user_query:
            return jsonify({'message': 'User Invalid'}), 400
        
        post_query = session.query(Posts).filter(Posts.post_id == post_id)
        if not post_query:
            return jsonify({'message': 'No related post found'}), 400
        
        bookmark_query = session.query(Bookmarks).join(UserDetails).filter(UserDetails.account_id == account_id, Bookmarks.post_id == post_id).first()
        if bookmark_query:
            return jsonify({'message': 'Post already bookmarked by the user'}), 400
        
        add_bookmark = Bookmarks(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id
        )
        
        # if data.get('')
        
        session.add(add_bookmark)
        session.commit()
        
        # data = add_like.serialize()
        
        return api_response(
            status_code=200,
            message="Post successfully bookmarked",
            data=add_bookmark.serialize(full=False)
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
        
def remove_bookmark(account_id, post_id):
    session = Session()
    
    try:
        bookmark_to_delete = session.query(Bookmarks).join(UserDetails).filter(UserDetails.account_id == account_id, Bookmarks.post_id == post_id).first()
        session.delete(bookmark_to_delete)
        session.commit()
        
        return api_response(
            status_code=200,
            message="Bookmark successfully removed",
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
    
def get_bookmark_by_account_id(account_id):
    session = Session()
    
    try:
        bookmark_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not bookmark_query:
            return jsonify({'message': 'User Invalid'}), 400
        data = [bookmark_query.serialize() for bookmark_query in bookmark_query]
        return api_response(status_code=200, message="bookmarks retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
    