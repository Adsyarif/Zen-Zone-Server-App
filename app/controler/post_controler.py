from flask import  request
from sqlalchemy import func
from app.models.posts import Posts
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from app.models.bookmarks import Bookmarks
from app.models.like import Like
from app.models.comments import Comments
from app.models.user_details import UserDetails
from sqlalchemy.orm import joinedload

def get_all_post():
    session = Session()
    try:
        posts = session.query(Posts).options(
            joinedload(Posts.like).joinedload(Like.user_details), 
            joinedload(Posts.comments),
            joinedload(Posts.bookmarks)
        ).all()
        
        if not posts:
            return api_response(status_code=404, message="No posts found", data={})
    
        post_data = []

        for post in posts:
            like_count = session.query(func.count(Like.like_id)).filter_by(post_id=post.post_id).scalar()
            comment_count = session.query(func.count(Comments.comment_id)).filter_by(post_id=post.post_id).scalar()
            bookmark_count = session.query(func.count(Bookmarks.bookmark_id)).filter_by(post_id=post.post_id).scalar()

            likes_details = [
                {
                    'user_id': like.user_id,
                    'user_name': like.user_details.user_name,
                    'liked_at': like.created_at
                }
                for like in post.like if like.user_details
            ]

            post_info = post.serialize(full=True)
            post_info.update({
                'like_count': like_count,
                'comment_count': comment_count,
                'bookmark_count': bookmark_count,
                'likes_details': likes_details
            })

            post_data.append(post_info)

        return api_response(status_code=200, message="Posts retrieved successfully", data=post_data)
    
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def get_post_by_id(post_id):
    session = Session()
    try:
        post = session.query(Posts).filter_by(post_id=post_id).first()
        if not post:
            return api_response(status_code=404, message="Post not found", data={})

        like_count = session.query(func.count(Like.like_id)).filter_by(post_id=post_id).scalar()
        comment_count = session.query(func.count(Comments.comment_id)).filter_by(post_id=post_id).scalar()
        bookmark_count = session.query(func.count(Bookmarks.bookmark_id)).filter_by(post_id=post_id).scalar()

        data = post.serialize()
        data.update({
            'like_count': like_count,
            'comment_count': comment_count,
            'bookmark_count': bookmark_count
        })

        return api_response(status_code=200, message="Post retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def create_post(account_id):
    session = Session()
    try:
        data = request.get_json()
        content = data.get('content')

        if not content:
            return api_response(status_code=400, message="Missing content", data={})

        user = session.query(UserDetails).filter_by(account_id=account_id).first()
        if user is None:
            return api_response(status_code=404, message="User not found", data={})

        new_post = Posts(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            content=content
            )
        session.add(new_post)
        session.commit()

        return api_response(status_code=201, message="Post created successfully", data=new_post.serialize())

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()


def soft_delete_post(post_id):
    session = Session()
    try:
        account_id = request.json.get('account_id')
        if not account_id:
            return api_response(status_code=400, message="Account ID is required", data={})

        user_details = session.query(UserDetails).filter_by(
            account_id=account_id).first()
        if not user_details:
            return api_response(status_code=404, message="User not found", data={})

        post = session.query(Posts).filter_by(post_id=post_id).first()
        if not post:
            return api_response(status_code=404, message="Post not found", data={})

        if post.user_id != user_details.user_id:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to delete this post", data={})

        if post.deleted_at is not None:
            return api_response(status_code=400, message="Post already deleted", data={})

        post.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Post soft deleted successfully", data=post.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def delete_post_by_id(post_id):
    session = Session()
    try:
        post = session.query(Posts).filter_by(post_id=post_id).first()
        if not post:
            return api_response(status_code=404, message="Post not found", data={})

        session.delete(post)
        session.commit()

        return api_response(status_code=200, message="Post deleted successfully", data={})
    except Exception as e:

        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def get_post_by_account_id(account_id):
    session = Session()
    try:
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()

        if not user_query:
            return api_response(
                status_code=200,
                message="User has no likes yet or user does not exist",
                data=[]
            )
        post = session.query(Posts).filter(Posts.user_id == user_query.user_id).all()
        data = [post.serialize(True) for post in post]

        if not data:
            return api_response(
                status_code=200,
                message="User has no post yet",
                data=[]
            )

        return api_response(
            status_code=200,
            message="post retrieved successfully",
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




