from flask import Blueprint
from app.controler.article_content_controler import get_artilce_content_by_article_id, create_article_content,delete_article_content, edit_article_content, get_all_article_content

articles_content_routes = Blueprint('articles_content', __name__)

articles_content_routes.route("/articles/content", methods=["GET"])(get_all_article_content)
articles_content_routes.route("/articles/content/<int:article_id>", methods=["GET"])(get_artilce_content_by_article_id)
articles_content_routes.route("/articles/content/create/<int:article_id>", methods=["POST"])(create_article_content)
articles_content_routes.route("/articles/content/<int:article_content_id>", methods=["PUT"])(edit_article_content)
articles_content_routes.route("/articles/content/<int:article_content_id>", methods=["DELETE"])(delete_article_content)
