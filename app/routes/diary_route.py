from flask import Blueprint

from app.controler.diary_controler import get_all_diary

diary_routes = Blueprint('diary', __name__)

diary_routes.route("/diary", methods=["GET"])(get_all_diary)