from flask import Blueprint
from app.controler.articles_controler import get_all_articles, get_articles_by_article_id, get_articles_by_tag, create_article, delete_article

articles_routes = Blueprint('articles', __name__)

articles_routes.route("/articles", methods=["GET"])(get_all_articles)
articles_routes.route("/articles/<int:article_id>", methods=["GET"])(get_articles_by_article_id)
articles_routes.route("/articles/tag/<string:tag>", methods=["GET"])(get_articles_by_tag)
articles_routes.route("/articles/create", methods=["POST"])(create_article)
articles_routes.route("/articles/<int:article_id>", methods=["DELETE"])(delete_article)

