from flask import Blueprint
from app.controler.review_counselor_controler import (
    get_all_review_counselor, 
    created_review_counselor,
    soft_delete_review_counselor,
    get_review_counselor_id,
    get_count_all_rating_total_by_counselor_id,
    get_average_rating_by_counselor_id
    )


review_counselor_routes = Blueprint('review_counselor', __name__)

review_counselor_routes.route("/review_counselor", methods=["GET"])(get_all_review_counselor)
review_counselor_routes.route("/review_counselor/<int:account_id>/<int:account_id_counselor>", methods=["POST"])(created_review_counselor)
review_counselor_routes.route("/review_counselor/<int:review_counselor_id>/delete", methods=["PUT"])(soft_delete_review_counselor)
review_counselor_routes.route("/review_counselor/<int:account_id_counselor>", methods=["GET"])(get_review_counselor_id)

review_counselor_routes.route("/review_counselor/<int:account_id_counselor>/total_ratings", methods=["GET"])(get_count_all_rating_total_by_counselor_id)
review_counselor_routes.route("/review_counselor/<int:account_id_counselor>/average_ratings", methods=["GET"])(get_average_rating_by_counselor_id)