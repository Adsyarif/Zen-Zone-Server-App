import os
from dotenv import load_dotenv
from flask import Flask
from app.routes.user_details_route import user_details_routes
from app.routes.gender_route import gender_routes
from app.routes.account_route import account_routes
from app.routes.roles_route import roles_routes

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(user_details_routes)
app.register_blueprint(gender_routes)
app.register_blueprint(account_routes)
app.register_blueprint(roles_routes)

if __name__ == "__main__":
    app.run(debug=True)