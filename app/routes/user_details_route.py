from flask import Blueprint
from app.controler.user_details_controler import (
    get_user_details,
    get_user_details_id,
    create_user_details,
    edit_user_details
)
user_details_routes = Blueprint('user_details', __name__)

user_details_routes.route("/user_details", methods=["GET"])(get_user_details)
user_details_routes.route("/user_details/<int:account_id>", methods=["GET"])(get_user_details_id)
user_details_routes.route("/user_details/<int:account_id>", methods=["POST"])(create_user_details)
user_details_routes.route("/user_details/<int:account_id>", methods=["PUT"])(edit_user_details)




