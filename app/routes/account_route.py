from flask import Blueprint

from app.controler.account_controler import (
    get_all_accounts,
    create_account, 
    login_account
)

account_routes = Blueprint('account', __name__)

account_routes.route("/account", methods=["GET"])(get_all_accounts)

account_routes.route("/account/signup", methods=["POST"])(create_account)

account_routes.route("/account/login", methods=["POST"])(login_account)