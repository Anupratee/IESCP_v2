from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

DB_NAME = 'Connectora.db'

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
