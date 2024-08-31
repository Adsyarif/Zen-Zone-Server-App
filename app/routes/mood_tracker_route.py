from flask import Blueprint

from app.controler.mood_tracker_controler import get_mood_tracker_by_account_id

mood_tracker_routes = Blueprint('mood_tracker', __name__)

mood_tracker_routes.route("/mood_tracker/<int:account_id>", methods=["GET"])(get_mood_tracker_by_account_id)