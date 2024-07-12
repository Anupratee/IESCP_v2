from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from os import path
from connectora.models import DB_NAME, db, ma, bcrypt
from connectora.utils import API_KEY, API_SECRET, CLOUD_NAME, create_admin

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mad2connectora'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'audiowavemad2'
    app.config['CLOUDINARY_URL'] = f"cloudinary://{API_KEY}:{API_SECRET}@{CLOUD_NAME}"

    app.static_folder = 'static'
    UPLOAD_FOLDER = app.static_folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    upload_folder_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder_path):
        os.makedirs(upload_folder_path)

    jwt = JWTManager(app)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    CORS(app, supports_credentials = True)

    with app.app_context():
        if not path.exists('backend/instance/' + DB_NAME):
            db.create_all()
            print('created database')
            try:
                create_admin()
            except Exception as e:
                pass

    app.app_context().push()

    from connectora.authAPI import authAPI

    app.register_blueprint(authAPI, url_prefix = '/')

    return app
    