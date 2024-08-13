from flask import Blueprint

from app.controler.bookmark_controler import get_all_bookmarks, do_bookmark_post, remove_bookmark, get_bookmark_by_account_id

bookmarks_routes = Blueprint('bookmarks', __name__)

bookmarks_routes.route("/bookmarks", methods=["GET"])(get_all_bookmarks)

bookmarks_routes.route("/bookmarks/<int:account_id>/<int:post_id>", methods=["POST"])(do_bookmark_post)
bookmarks_routes.route("/bookmarks/<int:account_id>", methods=["GET"])(get_bookmark_by_account_id)
bookmarks_routes.route("/bookmarks/<int:account_id>/<int:post_id>", methods=["DELETE"])(remove_bookmark)