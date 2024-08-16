from flask import Blueprint

from app.controler.diary_controler import get_all_diary, get_diary_by_id, create_diary_entry, edit_diary_by_id, soft_delete_diary_entry_by_id, get_diary_by_account_id

diary_routes = Blueprint('diary', __name__)

diary_routes.route("/diary", methods=["GET"])(get_all_diary)
diary_routes.route("/diary/<int:account_id>/<int:diary_id>", methods=["GET"])(get_diary_by_id)
diary_routes.route("/diary/<int:account_id>/create", methods=["POST"])(create_diary_entry)
diary_routes.route("/diary/<int:account_id>/<int:diary_id>/edit", methods=["PUT"])(edit_diary_by_id)
diary_routes.route("/diary/<int:account_id>/<int:diary_id>/delete", methods=["DELETE"])(soft_delete_diary_entry_by_id)
diary_routes.route("/diary/<int:account_id>", methods=["GET"])(get_diary_by_account_id)