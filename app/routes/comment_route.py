from flask import Blueprint

from app.controler.comments_controler import (
    get_all_comments,
    get_comments_by_post,
    create_comments_by_post,
    soft_delete_comment,
    get_notif_comment
)

comments_routes = Blueprint('comments', __name__)

comments_routes.route("/comments", methods=["GET"])(get_all_comments)
comments_routes.route("/comments/<int:account_id>/<int:post_id>", methods=["POST"])(create_comments_by_post)
comments_routes.route("/comments/<int:post_id>", methods=["GET"])(get_comments_by_post)
comments_routes.route("/comments/delete/<int:account_id>/<int:comment_id>", methods=["POST"])(soft_delete_comment)
comments_routes.route("/notification/comments/<int:account_id>", methods=["GET"])(get_notif_comment)