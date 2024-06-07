from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__, static_folder='../assets', )
app.config.from_object(Config)

if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'])):
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO']), )

if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_IMAGE'])):
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_IMAGE']), )

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
schema = Marshmallow(app)

from app import routes, response
from app.model import user