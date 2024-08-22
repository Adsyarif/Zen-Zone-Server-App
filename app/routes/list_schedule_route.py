from flask import Blueprint
from app.controler.list_schedule_controler import get_all_schedule

list_scedule_routes = Blueprint('scedule', __name__)

list_scedule_routes.route("/scedule", methods=["GET"])(get_all_schedule)
