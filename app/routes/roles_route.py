from flask import Blueprint
from app.controler.role_controler import get_all_roles

roles_routes = Blueprint('roles', __name__)

roles_routes.route("/roles", methods=["GET"])(get_all_roles)

