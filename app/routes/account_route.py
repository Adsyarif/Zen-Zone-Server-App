from flask import Blueprint

from app.controler.account_controler import get_all_accounts

account_routes = Blueprint('account', __name__)

account_routes.route("/account", methods=["GET"])(get_all_accounts)