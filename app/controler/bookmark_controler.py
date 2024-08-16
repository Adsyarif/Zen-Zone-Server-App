from flask import jsonify
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
        bookmark_query = session.query(Posts).filter(Posts.post_id == post_id)
        if not bookmark_query:
            return jsonify({'message': 'No related bookmark found'}), 400
        
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not user_query:
            return jsonify({'message': 'User not found'}), 400
        
        bookmar_query = (
            session.query(Bookmarks)
            .join(UserDetails)
            .filter(UserDetails.account_id == account_id, Bookmarks.post_id == post_id)
            .first()
        )
        
        if bookmar_query:
            return jsonify({'message': 'Post already liked by the user'}), 400
        
        add_bookmark = Bookmarks(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id
        )
        
        session.add(add_bookmark)
        session.commit()
        
        return api_response(
            status_code=200,
            message="Post successfully Bookmark",
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
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()

        if not user_query:
            return api_response(
                status_code=200,
                message="User has no bookmarks yet or user does not exist",
                data=[]
            )

        bookmark_query = session.query(Bookmarks).filter(Bookmarks.user_id == user_query.user_id).all()
        data = [bookmark.serialize(True) for bookmark in bookmark_query]

        if not data:
            return api_response(
                status_code=200,
                message="User has no bookmarks yet",
                data=[]
            )

        return api_response(
            status_code=200,
            message="Bookmarks retrieved successfully",
            data=data
        )
    except Exception as e:
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()
    