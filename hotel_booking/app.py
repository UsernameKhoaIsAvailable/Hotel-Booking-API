from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345678@localhost:3306/hotel_booking"
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)
app.register_blueprint(api_bp)