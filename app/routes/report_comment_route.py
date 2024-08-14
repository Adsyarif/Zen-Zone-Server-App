from flask import Blueprint

from app.controler.report_comment_controler import (
    get_all_report_comment,
    do_report_comment
)

report_comment_routes = Blueprint('/report_comment', __name__)

report_comment_routes.route("/report_comment", methods=["GET"])(get_all_report_comment)
report_comment_routes.route("/report_comment/<int:account_id>/<int:comment_id>", methods=["POST"])(do_report_comment)