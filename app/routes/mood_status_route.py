from flask import Blueprint

from app.controler.mood_status_controler import get_all_mood_status, get_mood_status_by_status_id

mood_status_routes = Blueprint('mood_status', __name__)

mood_status_routes.route("/mood_status", methods=["GET"])(get_all_mood_status)

mood_status_routes.route("/mood_status/<int:status_id>", methods=["GET"])(get_mood_status_by_status_id)