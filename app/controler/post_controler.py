from flask import Blueprint, request
from sqlalchemy import func
from app.models.posts import Posts
from app.connector.sql_connector import Session
from app.utils.api_response import api_response
from app.models.bookmarks import Bookmarks
from app.models.like import Like
from app.models.comments import Comments


def get_all_post():
    session = Session()
    try:
        posts = session.query(Posts).filter(Posts.deleted_at.is_(None)).all()

        if not posts:
            return api_response(status_code=404, message="No posts found", data={})

        post_data = []

        for post in posts:
            like_count = session.query(func.count(Like.like_id)).filter_by(
                post_id=post.post_id).scalar()
            comment_count = session.query(func.count(Comments.comment_id)).filter_by(
                post_id=post.post_id).scalar()
            bookmark_count = session.query(func.count(Bookmarks.bookmark_id)).filter_by(
                post_id=post.post_id).scalar()

            post_info = post.serialize(full=False)
            post_info.update({
                'like_count': like_count,
                'comment_count': comment_count,
                'bookmark_count': bookmark_count
            })

            post_data.append(post_info)

        sorted_data = sorted(
            post_data, key=lambda x: x['like_count'], reverse=True)

        return api_response(status_code=200, message="Posts retrieved successfully", data=sorted_data)

    except Exception as e:
        return api_response(status_code=500, message=f"Server error: {e}", data={})

    finally:
        session.close()


def get_post_by_id(post_id):
    session = Session()
    try:
        post = session.query(Posts).filter_by(
            post_id=post_id, deleted_at=None).first()
        if not post:
            return api_response(status_code=404, message="Post not found", data={})

        like_count = session.query(func.count(Like.like_id)).filter_by(
            post_id=post_id).scalar()
        comment_count = session.query(func.count(
            Comments.comment_id)).filter_by(post_id=post_id).scalar()
        bookmark_count = session.query(func.count(
            Bookmarks.bookmark_id)).filter_by(post_id=post_id).scalar()

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


def create_post():
    session = Session()
    try:
        data = request.json
        if 'account_id' not in data or 'content' not in data:
            return api_response(status_code=400, message="Missing 'account_id' or 'content' in request", data={})

        user_details = session.query(UserDetails).filter_by(
            account_id=data['account_id']).first()
        if not user_details:
            return api_response(status_code=404, message="User not found", data={})

        new_post = Posts(
            user_id=user_details.user_id,
            content=data['content'],
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


def update_post(post_id):
    session = Session()
    try:
        account_id = request.json.get('account_id')
        content = request.json.get('content')

        if not account_id:
            return api_response(status_code=400, message="Account ID is required", data={})

        if not content:
            return api_response(status_code=400, message="Content is required", data={})

        user_details = session.query(UserDetails).filter_by(
            account_id=account_id).first()
        if not user_details:
            return api_response(status_code=404, message="User not found", data={})

        post = session.query(Posts).filter_by(post_id=post_id).first()
        if not post:
            return api_response(status_code=404, message="Post not found", data={})

        if post.user_id != user_details.user_id:
            return api_response(status_code=403, message="Unauthorized: You are not allowed to update this post", data={})

        if post.deleted_at is not None:
            return api_response(status_code=400, message="Post is deleted and cannot be updated", data={})

        post.content = content
        session.commit()

        return api_response(status_code=200, message="Post updated successfully", data=post.serialize(full=True))

    except Exception as e:
        session.rollback()
        return api_response(status_code=500, message=f"Server error: {e}", data={})
    finally:
        session.close()
