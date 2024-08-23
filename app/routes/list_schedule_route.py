from flask import Blueprint
from app.controler.list_schedule_controller import get_all_list_schedules

list_scedule_routes = Blueprint('list_schedule', __name__)

list_scedule_routes.route("/list_schedule", methods=["GET"])(get_all_list_schedules)

