from app import response, app, db
from flask import request, jsonify, url_for
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
import uuid, os, datetime
from app.request.DataModel.DataTestStoreRequest import DataTestStoreRequest

def store():
    request_data = DataTestStoreRequest()
    
    if not request_data.validate():
        return response.error(422, 'Invalid request form validation', request_data.errors)
    
    try:
        file = request_data.file.data
        filename = secure_filename(file.filename)
        new_filename = f'Video-{str(uuid.uuid4())}{filename}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], new_filename)
        file.save(file_path)
        # Construct the URL path to the uploaded video file
        # url_path = url_for('static', filename=new_filename)
        return response.success(200, 'Ok', {
            "url_path": os.path.join(request.host_url, file_path).replace('\\', '/'),
        })
    except Exception as e:
        return response.error(message=str(e))

