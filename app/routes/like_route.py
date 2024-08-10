from flask import Blueprint

from app.controler.like_controler import get_all_like, do_like_post, remove_like

like_routes = Blueprint('like', __name__)

like_routes.route("/like", methods=["GET"])(get_all_like)

like_routes.route("/like/<int:user_id>/<int:post_id>", methods=["POST"])(do_like_post)

like_routes.route("/like/<int:like_id>", methods=["DELETE"])(remove_like)