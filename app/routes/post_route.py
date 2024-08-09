from flask import Blueprint

from app.controler.post_controler import get_all_post

post_routes = Blueprint('post', __name__)

post_routes.route("/post", methods=["GET"])(get_all_post)