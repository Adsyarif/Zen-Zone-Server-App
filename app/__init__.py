import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.user_details_route import user_details_routes
from app.routes.gender_route import gender_routes
from app.routes.account_route import account_routes
from app.routes.roles_route import roles_routes
from app.routes.post_route import post_routes
from app.routes.report_category_route import report_category_routes
from app.routes.report_comment_route import report_comment_routes
from app.routes.report_post_route import report_post_routes
from app.routes.comment_route import comments_routes
from app.routes.bookmarks_route import bookmarks_routes
from app.routes.diary_route import diary_routes
from app.routes.bookmarks_route import bookmarks_routes
from app.routes.mood_category_route import mood_category_routes
from app.routes.mood_status_route import mood_status_routes
from app.routes.mood_tracker_route import mood_tracker_routes
from app.routes.like_route import like_routes
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

CORS(app, origins=['http://localhost:5000'
], supports_credentials=True)

@app.route("/")
def hello_world():
    return "Hello, World! welcome to Zen-zone"

app.register_blueprint(user_details_routes)
app.register_blueprint(gender_routes)
app.register_blueprint(account_routes)
app.register_blueprint(roles_routes)
app.register_blueprint(post_routes)
app.register_blueprint(report_category_routes)
app.register_blueprint(report_comment_routes)
app.register_blueprint(report_post_routes)
app.register_blueprint(comments_routes)
app.register_blueprint(bookmarks_routes)
app.register_blueprint(diary_routes)
app.register_blueprint(mood_category_routes)
app.register_blueprint(mood_status_routes)
app.register_blueprint(mood_tracker_routes)
app.register_blueprint(like_routes)

if __name__ == "__main__":
    app.run()