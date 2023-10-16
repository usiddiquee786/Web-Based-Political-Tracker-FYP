from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from os import path
import json
from flask_pymongo import PyMongo
# from flask_login import LoginManager
app = Flask(__name__, static_url_path='/static')
# db = SQLAlchemy()
# DB_NAME = "database.db"
app.config["MONGO_URI"] = "mongodb://localhost:27017/tweets"
mongo = PyMongo(app)

def create_app():
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # db.init_app(app)
    

    from .views import views
    from .auth import auth
    from .extra import extra

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(extra, url_prefix='/')

    return app