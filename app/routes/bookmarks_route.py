from flask import Blueprint

from app.controler.bookmark_controler import get_all_bookmarks

bookmarks_routes = Blueprint('bookmarks', __name__)

bookmarks_routes.route("/bookmarks", methods=["GET"])(get_all_bookmarks)