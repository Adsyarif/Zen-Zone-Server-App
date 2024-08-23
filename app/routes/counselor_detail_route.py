from flask import Blueprint
from app.controler.counselor_detail_controller import get_all_counselor_detail, get_counselor_detail_by_id, create_new_counselor_id, update_counselor_detail_by_id

counselor_detail_routes = Blueprint('counselor_details', __name__)

counselor_detail_routes.route("/counselors", methods=["GET"])(get_all_counselor_detail)
counselor_detail_routes.route("/counselor/<int:account_id>/<int:counselor_id>", methods=["GET"])(get_counselor_detail_by_id)
counselor_detail_routes.route("/counselor/create/<int:account_id>", methods=["POST"])(create_new_counselor_id)
counselor_detail_routes.route("/counselor/edit/<int:account_id>/<int:counselor_id>", methods=["PUT"])(update_counselor_detail_by_id)