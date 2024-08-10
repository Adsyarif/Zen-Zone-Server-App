from flask import Blueprint, request, jsonify
from app.models.bookmarks import Bookmarks
from app.models.posts import Posts
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
        
def do_bookmark_post(user_id, post_id):
    session = Session()
    try:
        # data = request.json
        
        post_query = session.query(Posts).filter(Posts.user_id == user_id)
        if not post_query:
            return jsonify({'message': 'No related post found'}), 400
        
        bookmark_query = session.query(Bookmarks).filter(Bookmarks.user_id == user_id, Bookmarks.post_id == post_id).first()
        if bookmark_query:
            return jsonify({'message': 'Post already bookmarked by the user'}), 400
        
        add_bookmark = Bookmarks(
            user_id=user_id,
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
        
def remove_bookmark(bookmark_id):
    session = Session()
    
    try:
        bookmark_to_delete = session.query(Bookmarks).filter(Bookmarks.bookmark_id == bookmark_id).first()
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
    