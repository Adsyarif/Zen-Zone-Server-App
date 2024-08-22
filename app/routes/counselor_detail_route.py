from flask import Blueprint
from app.controler.counselor_detail_controller import get_all_counselor_detail

counselor_detail_routes = Blueprint('counselor_details', __name__)

counselor_detail_routes.route("/counselor_details", methods=["GET"])(get_all_counselor_detail)