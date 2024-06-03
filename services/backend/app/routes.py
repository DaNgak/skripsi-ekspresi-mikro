from app import app, response
from app.controller import UserController, DataModelController
from flask import request, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash
import os

@app.route('/')
def index():
    # return generate_password_hash(password='password')
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return UserController.login()
    else:
        return response.error(405, "Method Not Allowed")

@app.route('/data-model/datatest', methods=['POST'])
def upload():
    if request.method == 'POST':
        return DataModelController.store()
    else:
        return response.error(405, "Method Not Allowed")

@app.route('/auth', methods=['GET'])
@jwt_required()
def auth():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return response.success(current_user, "Success!")
    else:
        return response.error(405, "Method Not Allowed")
    
@app.route('/images/<name>')
def display_file(name):
    # return app.config["UPLOAD_FOLDER"] + '/' + name
    return os.path.join(app.config["UPLOAD_FOLDER"], name).replace('\\', '/')
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)