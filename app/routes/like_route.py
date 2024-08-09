from flask import Blueprint

from app.controler.like_controler import get_all_like

like_routes = Blueprint('like', __name__)

like_routes.route("/like", methods=["GET"])(get_all_like)