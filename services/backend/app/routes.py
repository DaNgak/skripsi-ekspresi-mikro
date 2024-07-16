from app import app, response
from app.controller import UserController, DataModelController, TestingModelController
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

@app.route('/data-model/data-test', methods=['POST'])
def upload():
    if request.method == 'POST':
        return DataModelController.store()
    else:
        return response.error(405, "Method Not Allowed")
    
@app.route('/testing', methods=['POST'])
def testing():
    if request.method == 'POST':
        return TestingModelController.testing()
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