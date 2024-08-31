from flask import Blueprint
from app.controler.list_schedule_controller import (
    get_all_list_schedules, 
    get_schedule_by_counselor_id, 
    post_schedule_by_counselor_id, 
    put_user_booked_by_account_id, 
    put_counselor_reschedule_by_schedule_id, 
    put_cancel_by_account_id, 
    put_update_status_by_counselor_id , 
    delete_schedule_by_counselor_id,
    get_schedule_by_booked_by_account_id,
    mark_schedule_as_done,
    mark_schedule_as_done_by_user
    )

list_scedule_routes = Blueprint('list_schedule', __name__)

list_scedule_routes.route("/list_schedule", methods=["GET"])(get_all_list_schedules)
list_scedule_routes.route("/list_schedule/<int:counselor_id>", methods=["GET"])(get_schedule_by_counselor_id)
list_scedule_routes.route("/list_schedule/<int:counselor_id>", methods=["POST"])(post_schedule_by_counselor_id)
list_scedule_routes.route("/list_schedule/book/<int:account_id>/<int:schedule_id>", methods=["PUT"])(put_user_booked_by_account_id)
list_scedule_routes.route("/list_schedule/cancel/<int:account_id>/<int:schedule_id>", methods=["PUT"])(put_cancel_by_account_id)
list_scedule_routes.route("/list_schedule/reschedule/<int:counselor_id>/<int:schedule_id>", methods=["PUT"])(put_counselor_reschedule_by_schedule_id)
list_scedule_routes.route("/list_schedule/counselor/delete/<int:counselor_id>/<int:schedule_id>", methods=["DELETE"])(delete_schedule_by_counselor_id)

list_scedule_routes.route("/list_schedule/user/<int:booked_by_account_id>", methods=["GET"])(get_schedule_by_booked_by_account_id)
list_scedule_routes.route("/list_schedule/status/<int:counselor_id>/<int:schedule_id>", methods=["PUT"])(mark_schedule_as_done)
list_scedule_routes.route("/list_schedule/status/<int:account_id>/<int:schedule_id>/<int:counselor_id>", methods=["PUT"])(mark_schedule_as_done_by_user)