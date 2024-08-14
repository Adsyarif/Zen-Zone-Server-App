from flask import Blueprint

from app.controler.report_post_controler import (
    get_all_report_post,
    do_report_post
    )

report_post_routes = Blueprint('/report_post', __name__)

report_post_routes.route("/report_post", methods=["GET"])(get_all_report_post)
report_post_routes.route("/report_post/<int:account_id>/<int:post_id>", methods=["POST"])(do_report_post)