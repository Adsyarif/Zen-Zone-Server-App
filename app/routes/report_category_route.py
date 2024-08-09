from flask import Blueprint

from app.controler.report_category_controler import get_all_report_category

report_category_routes = Blueprint('/report_category', __name__)

report_category_routes.route("/report_category", methods=["GET"])(get_all_report_category)