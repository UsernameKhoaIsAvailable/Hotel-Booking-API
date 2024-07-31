import sqlalchemy
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345678@localhost:3306/hotel_booking"
api = Api(app)
# db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all()
        return '<h1>It works.</h1>'
    except:
        return '<h1>Something is broken.</h1>'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
