from flask import Blueprint

from app.controler.comments_controler import get_all_comments

comments_routes = Blueprint('comments', __name__)

comments_routes.route("/comments", methods=["GET"])(get_all_comments)