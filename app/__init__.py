from flask import Flask
from app.connector.sql_connector import connection

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
