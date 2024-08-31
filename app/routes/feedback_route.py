from flask import Blueprint

from app.controler.feedback_controler import (
    get_all_feedback, 
    get_feedback_by_id, 
    create_feedback_entry, 
    edit_feedback_by_id, 
    soft_delete_feedback_entry_by_id, 
    get_feedback_by_account_id
    )

feedback_routes = Blueprint('feedback', __name__)

feedback_routes.route("/feedback", methods=["GET"])(get_all_feedback)
feedback_routes.route("/feedback/<int:account_id>/<int:feedback_id>", methods=["GET"])(get_feedback_by_id)
feedback_routes.route("/feedback/<int:account_id>/<int:feedback_id>", methods=["GET"])(get_feedback_by_id)
feedback_routes.route("/feedback/<int:account_id>/create", methods=["POST"])(create_feedback_entry)
feedback_routes.route("/feedback/<int:account_id>/<int:feedback_id>/edit", methods=["PUT"])(edit_feedback_by_id)
feedback_routes.route("/feedback/<int:account_id>/<int:feedback_id>/delete", methods=["DELETE"])(soft_delete_feedback_entry_by_id)
feedback_routes.route("/feedback/<int:account_id>", methods=["GET"])(get_feedback_by_account_id)