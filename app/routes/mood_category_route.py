from flask import Blueprint

from app.controler.mood_category_controler import get_all_mood_category

mood_category_routes = Blueprint('mood_category', __name__)

mood_category_routes.route("/mood_category", methods=["GET"])(get_all_mood_category)