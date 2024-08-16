from flask import  request, jsonify
from sqlalchemy import func
from flask import  request, jsonify
from sqlalchemy import func
from app.models.comments import Comments
from app.models.posts import Posts
from app.models.user_details import UserDetails
from app.models.posts import Posts
from app.models.user_details import UserDetails
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from sqlalchemy.orm import joinedload

def get_all_comments():
    session = Session()
    try:
        comments = session.query(Comments).all()
        data = [comments.serialize() for comments in comments]
        return api_response(status_code=200, message="Accounts retrieved successfully", data=data)
    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def get_comments_by_post(post_id):
    session = Session()
    try:

        comments = session.query(Comments).filter(Comments.post_id == post_id).all()

        if not comments:
            return api_response(status_code=404, message="No comments found for this post", data={})

        data = [comment.serialize() for comment in comments]

        return api_response(status_code=200, message="Comments retrieved successfully", data=data)

    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def create_comments_by_post(account_id, post_id):
    session = Session()
    try:
        data = request.get_json()
        content = data.get('content') 
        
        post = session.query(Posts).filter(Posts.post_id == post_id).first()
        if post is None:
            return jsonify({'message': 'No related post found'}), 400

        if not content:
            return api_response(status_code=400, message="Missing content", data={})

        user = session.query(UserDetails).filter_by(account_id=account_id).first()
        if user is None:
            return api_response(status_code=404, message="User not found", data={})

        new_comment= Comments(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id,
            content=content
        )
        session.add(new_comment)
        session.commit()

        return api_response(status_code=201, message="Comment created successfully", data={"comment_id": new_comment.comment_id})

    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def soft_delete_comment(account_id, comment_id):
    session = Session()
    try:
        comment = session.query(Comments).filter_by(comment_id=comment_id).first()
        if not comment:
            return api_response(status_code=404, message="Post not found", data={})

        if comment.user_details.account_id != account_id:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to delete this post", data={})

        if comment.deleted_at is not None:
            return api_response(status_code=400, message="Post already deleted", data={})

        comment.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Post soft deleted successfully", data=comment.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def get_notif_comment(account_id):
    session = Session()
    try:
        user = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()
        if not user:
            return jsonify({
                'status': {
                    'code': 404,
                    'message': 'User not found'
                },
                'data': []
            })

        user_id = user.user_id

        posts = session.query(Posts).filter(Posts.user_id == user_id).options(
            joinedload(Posts.comments).joinedload(Comments.user_details)  
        ).all()

        if not posts:
            return jsonify({
                'status': {
                    'code': 404,
                    'message': 'No posts found for this user'
                },
                'data': []
            })

        Comments_data = []
        for post in posts:
            for comments in post.comments:
                if comments.user_details.account_id == account_id:
                    continue
                Comments_data.append({
                    'post_id': post.post_id,
                    'post_content': post.content,
                    'post_created_at': post.created_at,
                    'comment_id': comments.comment_id,
                    'user_id': comments.user_id,
                    'user_name': comments.user_details.user_name,
                    'created_at': comments.created_at,
                    'content':comments.content
                })

        return jsonify({
            'status': {
                'code': 200,
                'message': 'Likes retrieved successfully'
            },
            'data': Comments_data
        })

    except Exception as e:
        return jsonify({
            'status': {
                'code': 500,
                'message': f'Server error: {e}'
            },
            'data': []
        })
    
    finally:
        session.close()

def get_comments_by_post(post_id):
    session = Session()
    try:

        comments = session.query(Comments).filter(Comments.post_id == post_id).all()

        if not comments:
            return api_response(status_code=404, message="No comments found for this post", data={})

        data = [comment.serialize() for comment in comments]

        return api_response(status_code=200, message="Comments retrieved successfully", data=data)

    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def create_comments_by_post(account_id, post_id):
    session = Session()
    try:
        data = request.get_json()
        content = data.get('content') 
        
        post = session.query(Posts).filter(Posts.post_id == post_id).first()
        if post is None:
            return jsonify({'message': 'No related post found'}), 400

        if not content:
            return api_response(status_code=400, message="Missing content", data={})

        user = session.query(UserDetails).filter_by(account_id=account_id).first()
        if user is None:
            return api_response(status_code=404, message="User not found", data={})

        new_comment= Comments(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id,
            content=content
        )
        session.add(new_comment)
        session.commit()

        return api_response(status_code=201, message="Comment created successfully", data={"comment_id": new_comment.comment_id})

    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    
    finally:
        session.close()

def soft_delete_comment(account_id, comment_id):
    session = Session()
    try:
        comment = session.query(Comments).filter_by(comment_id=comment_id).first()
        if not comment:
            return api_response(status_code=404, message="Post not found", data={})

        if comment.user_details.account_id != account_id:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to delete this post", data={})

        if comment.deleted_at is not None:
            return api_response(status_code=400, message="Post already deleted", data={})

        comment.deleted_at = func.now()
        session.commit()

        return api_response(status_code=200, message="Post soft deleted successfully", data=comment.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()

def get_notif_comment(account_id):
    session = Session()
    try:
        user = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()
        if not user:
            return jsonify({
                'status': {
                    'code': 404,
                    'message': 'User not found'
                },
                'data': []
            })

        user_id = user.user_id

        posts = session.query(Posts).filter(Posts.user_id == user_id).options(
            joinedload(Posts.comments).joinedload(Comments.user_details)  
        ).all()

        if not posts:
            return jsonify({
                'status': {
                    'code': 404,
                    'message': 'No posts found for this user'
                },
                'data': []
            })

        Comments_data = []
        for post in posts:
            for comments in post.comments:
                if comments.user_details.account_id == account_id:
                    continue
                Comments_data.append({
                    'post_id': post.post_id,
                    'post_content': post.content,
                    'post_created_at': post.created_at,
                    'comment_id': comments.comment_id,
                    'user_id': comments.user_id,
                    'user_name': comments.user_details.user_name,
                    'created_at': comments.created_at,
                    'content':comments.content
                })

        return jsonify({
            'status': {
                'code': 200,
                'message': 'Likes retrieved successfully'
            },
            'data': Comments_data
        })

    except Exception as e:
        return jsonify({
            'status': {
                'code': 500,
                'message': f'Server error: {e}'
            },
            'data': []
        })
    
    finally:
        session.close() 
