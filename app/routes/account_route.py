from flask import Blueprint

<<<<<<< HEAD
from app.controler.account_controler import (
    get_all_accounts,
    create_account, 
    login_account
)
=======
from app.controler.account_controler import get_all_accounts, create_account, login_account
>>>>>>> ff7a480 (feat:login-controler)

account_routes = Blueprint('account', __name__)

account_routes.route("/account", methods=["GET"])(get_all_accounts)

<<<<<<< HEAD
account_routes.route("/account/signup", methods=["POST"])(create_account)
=======
account_routes.route("/account/sigunp", methods=["POST"])(create_account)
>>>>>>> ff7a480 (feat:login-controler)

account_routes.route("/account/login", methods=["POST"])(login_account)