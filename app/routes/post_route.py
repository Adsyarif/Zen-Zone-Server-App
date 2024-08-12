from flask import Blueprint

from app.controler.post_controler import (
    get_all_post,
    get_post_by_id,
    create_post,
    soft_delete_post,
    update_post
)

post_routes = Blueprint('post', __name__)

post_routes.route("/post", methods=["GET"])(get_all_post)
post_routes.route("/post/<int:post_id>", methods=["GET"])(get_post_by_id)
post_routes.route("/post/create", methods=["POST"])(create_post)
post_routes.route("/post/<int:post_id>/delete",
                  methods=["DELETE"])(soft_delete_post)
post_routes.route("/post/<int:post_id>/update", methods=["PUT"])(update_post)
