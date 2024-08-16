from flask import Blueprint

from app.controler.post_controler import (
    get_all_post,
    get_post_by_id,
    create_post,
    soft_delete_post, 
    delete_post_by_id,
    get_post_by_account_id
    )

post_routes = Blueprint('post', __name__)

post_routes.route("/post", methods=["GET"])(get_all_post)
post_routes.route("/post/<int:post_id>", methods=["GET"])(get_post_by_id)
post_routes.route("/post/<int:account_id>", methods=["POST"])(create_post)
post_routes.route("/post/delete/<int:post_id>", methods=["POST"])(soft_delete_post)
post_routes.route("/delete/<int:post_id>", methods=["DELETE"])(delete_post_by_id)
post_routes.route("/post/get/<int:account_id>", methods=["GET"])(get_post_by_account_id)