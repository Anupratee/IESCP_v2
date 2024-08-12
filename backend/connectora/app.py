from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from os import path
import logging
from flask_mail import Mail
from flask_caching import Cache
from models import DB_NAME, db, ma, bcrypt
from utils import API_KEY, API_SECRET, CLOUD_NAME, create_admin, create_categories
from workers import celery, ContextTask

celery = celery   
celery.conf.update(
    BROKER_URL = 'redis://localhost:6379/1',
    RESULT_BACKEND = 'redis://localhost:6379/2'
    )
celery.Task = ContextTask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mad2connectora'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'audiowavemad2'
app.config['CLOUDINARY_URL'] = f"cloudinary://{API_KEY}:{API_SECRET}@{CLOUD_NAME}"
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
# app.config["CACHE_TYPE"] = "redis"
# app.config["CACHE_REDIS_URL"] = 'redis://localhost:6379/3'

app.static_folder = 'static'
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
upload_folder_path = app.config['UPLOAD_FOLDER']
if not os.path.exists(upload_folder_path):
    os.makedirs(upload_folder_path)

jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)
# cache.init_app(app)
bcrypt.init_app(app)
mail = Mail(app)

CORS(app, supports_credentials = True)

with app.app_context():
    instance_path = path.join(app.instance_path, DB_NAME)
    if not path.exists(instance_path):
        db.create_all()
        print('created database')
        try:
            create_admin()
            create_categories()
        except Exception as e:
            logging.error(f'Error during setup: {e}')
            db.session.rollback()

app.app_context().push()

from authAPI import authAPI
from campaignsAPI import campaignsAPI
from usersAPI import usersAPI
from influencersAPI import influencersAPI
from sponsorsAPI import sponsorsAPI
from adsAPI import adsAPI
from categoriesAPI import categoriesAPI
from adrequestsAPI import adrequestsAPI
from statsAPI import statsAPI

app.register_blueprint(authAPI, url_prefix = '/')
app.register_blueprint(campaignsAPI, url_prefix="/")
app.register_blueprint(usersAPI, url_prefix="/")
app.register_blueprint(influencersAPI, url_prefix="/")
app.register_blueprint(sponsorsAPI, url_prefix="/")
app.register_blueprint(adsAPI, url_prefix="/")
app.register_blueprint(categoriesAPI, url_prefix="/")
app.register_blueprint(adrequestsAPI, url_prefix="/")
app.register_blueprint(statsAPI, url_prefix="/")

if __name__ == '__main__':
    app.run(debug = True)
    