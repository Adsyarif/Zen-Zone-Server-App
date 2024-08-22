from flask import Blueprint
from app.controler.article_content_controler import get_all_article_content, get_artilce_content_by_article_id

articles_content_routes = Blueprint('articles_content', __name__)

articles_content_routes.route("/articles/content/<int:article_id>", methods=["GET"])(get_artilce_content_by_article_id)