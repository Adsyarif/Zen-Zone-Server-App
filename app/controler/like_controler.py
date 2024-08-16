from flask import  jsonify
from app.models.like import Like
from app.models.posts import Posts
from app.models.user_details import UserDetails
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from sqlalchemy.orm import joinedload

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
        post_query = session.query(Posts).filter(Posts.post_id == post_id)
        if not post_query:
            return jsonify({'message': 'No related post found'}), 400
        
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not user_query:
            return jsonify({'message': 'User not found'}), 400
        
        like_query = (
            session.query(Like)
            .join(UserDetails)
            .filter(UserDetails.account_id == account_id, Like.post_id == post_id)
            .first()
        )
        
        if like_query:
            return jsonify({'message': 'Post already liked by the user'}), 400
        
        add_like = Like(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id
        )
        
        session.add(add_like)
        session.commit()
        
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

def get_like_by_account_id(account_id):
    session = Session()
    try:
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()

        if not user_query:
            return api_response(
                status_code=200,
                message="User has no likes yet or user does not exist",
                data=[]
            )
        likes = session.query(Like).filter(Like.user_id == user_query.user_id).all()
        data = [like.serialize(True) for like in likes]

        if not data:
            return api_response(
                status_code=200,
                message="User has no likes yet",
                data=[]
            )

        return api_response(
            status_code=200,
            message="Likes retrieved successfully",
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

        
def remove_like(account_id, post_id):
    session = Session()
    try:
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()
        if not user_query:
            return jsonify({'message': 'User not found'}), 400

        like_query = session.query(Like).filter(
            Like.user_id == user_query.user_id,
            Like.post_id == post_id
        ).first()

        if not like_query:
            return jsonify({'message': 'Like not found'}), 400

        session.delete(like_query)
        session.commit()

        return api_response(
            status_code=200,
            message="Like successfully removed",
            data={}
        )
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()

def get_notif_like(account_id):
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
            joinedload(Posts.like).joinedload(Like.user_details)  
        ).all()

        if not posts:
            return jsonify({
                'status': {
                    'code': 404,
                    'message': 'No posts found for this user'
                },
                'data': []
            })
        likes_data = []
        for post in posts:
            for like in post.like:
                if like.user_details.account_id == account_id:
                    continue
                likes_data.append({
                    'post_id': post.post_id,
                    'post_content': post.content,
                    'post_created_at': post.created_at,
                    'like_id': like.like_id,
                    'user_id': like.user_id,
                    'user_name': like.user_details.user_name,
                    'liked_at': like.created_at
                })

        return jsonify({
            'status': {
                'code': 200,
                'message': 'Likes retrieved successfully'
            },
            'data': likes_data
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
        
def do_like_post(account_id, post_id):
    session = Session()
    try:
        post_query = session.query(Posts).filter(Posts.post_id == post_id)
        if not post_query:
            return jsonify({'message': 'No related post found'}), 400
        
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id)
        if not user_query:
            return jsonify({'message': 'User not found'}), 400
        
        like_query = (
            session.query(Like)
            .join(UserDetails)
            .filter(UserDetails.account_id == account_id, Like.post_id == post_id)
            .first()
        )
        
        if like_query:
            return jsonify({'message': 'Post already liked by the user'}), 400
        
        add_like = Like(
            user_id=session.query(UserDetails.user_id).filter(UserDetails.account_id == account_id).scalar(),
            post_id=post_id
        )
        
        session.add(add_like)
        session.commit()
        
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

def get_like_by_account_id(account_id):
    session = Session()
    try:
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()

        if not user_query:
            return api_response(
                status_code=200,
                message="User has no likes yet or user does not exist",
                data=[]
            )

        likes = session.query(Like).filter(Like.user_id == user_query.user_id).all()
        data = [like.serialize() for like in likes]

        if not data:
            return api_response(
                status_code=200,
                message="User has no likes yet",
                data=[]
            )

        return api_response(
            status_code=200,
            message="Likes retrieved successfully",
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

        
def remove_like(account_id, post_id):
    session = Session()
    try:
        user_query = session.query(UserDetails).filter(UserDetails.account_id == account_id).first()
        if not user_query:
            return jsonify({'message': 'User not found'}), 400

        like_query = session.query(Like).filter(
            Like.user_id == user_query.user_id,
            Like.post_id == post_id
        ).first()

        if not like_query:
            return jsonify({'message': 'Like not found'}), 400

        session.delete(like_query)
        session.commit()

        return api_response(
            status_code=200,
            message="Like successfully removed",
            data={}
        )
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=f"Server error: {str(e)}",
            data={}
        )
    finally:
        session.close()

def get_notif_like(account_id):
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
            joinedload(Posts.like).joinedload(Like.user_details)  
        ).all()

        if not posts:
            return jsonify({
                'status': {
                    'code': 404,
                    'message': 'No posts found for this user'
                },
                'data': []
            })
        likes_data = []
        for post in posts:
            for like in post.like:
                if like.user_details.account_id == account_id:
                    continue
                likes_data.append({
                    'post_id': post.post_id,
                    'post_content': post.content,
                    'post_created_at': post.created_at,
                    'like_id': like.like_id,
                    'user_id': like.user_id,
                    'user_name': like.user_details.user_name,
                    'liked_at': like.created_at
                })

        return jsonify({
            'status': {
                'code': 200,
                'message': 'Likes retrieved successfully'
            },
            'data': likes_data
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