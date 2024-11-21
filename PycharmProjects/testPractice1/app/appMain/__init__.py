from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()


def mydb():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password1234@localhost:5432/Testpractice"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'mythilikshathriya@gmail.com'
    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)
    return app


