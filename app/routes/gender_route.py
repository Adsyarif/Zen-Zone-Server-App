from flask import Blueprint

from app.controler.gender_controler import get_all_genders

gender_routes = Blueprint('gender', __name__)

gender_routes.route("/gender", methods=["GET"])(get_all_genders)