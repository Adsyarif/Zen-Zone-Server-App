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
        posts = session.query(Posts).all()

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
        post = session.query(Posts).filter_by(post_id=post_id).first()
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
