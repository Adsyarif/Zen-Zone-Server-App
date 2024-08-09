from flask import Blueprint

from app.controler.mood_tracker_controler import get_all_mood_tracker

mood_tracker_routes = Blueprint('mood_tracker', __name__)

mood_tracker_routes.route("/mood_tracker", methods=["GET"])(get_all_mood_tracker)