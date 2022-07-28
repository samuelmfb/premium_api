import json
from flask import Flask, jsonify
import os
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.auth import auth
from src.models.customers import customers
from src.models.expenses import expenses
from src.models.incomes import incomes
from src.models.producers import producers
from src.models.projects import projects
from src.models.tasks import tasks
from src.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config

app = Flask(__name__,
    instance_relative_config = True)

app.config.from_mapping(
    SECRET_KEY = os.environ.get("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),
    SWAGGER = {
        "title": "Premium Studio API",
        "uiversion": 3
    }
)

db.app = app
db.init_app(app)

JWTManager(app)
Swagger(app, config=swagger_config, template=template)
app.register_blueprint(auth)
app.register_blueprint(customers)
app.register_blueprint(expenses)
app.register_blueprint(incomes)
app.register_blueprint(producers)
app.register_blueprint(projects)
app.register_blueprint(tasks)

@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return jsonify({"error": "Not found."}), HTTP_404_NOT_FOUND

@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify({"error": "Server error."}), HTTP_500_INTERNAL_SERVER_ERROR

#Run
if __name__ == '__main__':
    app.run(debug = True)