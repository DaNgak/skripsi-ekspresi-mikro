from app.model.user import User
from app.resource.UserCollection import UserCollection
from app import response, app, db
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
import uuid, os, datetime
from app.request.Auth.LoginStoreRequest import LoginStoreRequest

def createUser():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        level = 1

        user = User(name=name, email=email, password=password, level=level)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()
        
        return response.success('', 'Success menambahkan data admin!')
    except Exception as e:
        print(e)
        return response.error(message=str(e))

def login():
    request_data = LoginStoreRequest()
    
    if not request_data.validate():
        # send message data invalid
        return response.error(422, 'Invalid request form validation', request_data.errors)

    try:
        email = request_data.email.data
        password = request_data.password.data

        user = User.query.filter_by(email=email).first()

        if not user or not user.checkPassword(password):
            return response.error(422, 'Invalid credentials!')

        data = UserCollection().dump(user)
        expires = datetime.timedelta(days=2)
        expires_refresh = datetime.timedelta(days=2)
        token = create_access_token(identity=data, fresh=True, expires_delta=expires)
        refresh_token = create_access_token(identity=data, expires_delta=expires_refresh)
        return response.success(200, 'Success login!', {
            'user': data,
            'token': token,
            'refresh_token': refresh_token
        }) 
    except Exception as e:
        return response.error(message=str(e))
    
def upload():
    request_data = (request.form)
    
    if not request_data.validate():
        return response.error(422, 'Invalid credentials!', request_data.errors)
    
    try:
        if 'file' not in request.files:
            return response.error([], '')
        
        file = request.files['file']
        if file.filename == '':
            return response.badRequest([], 'No selected file!')

        # if file and allowed_file(file.filename):
        #     uid = uuid.uuid4()
        #     filename = secure_filename(file.filename)
        #     renamefile = f'Flask-{str(uid)}{filename}'
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))
        #     uploads = Gambar(judul=judul, pathname=renamefile)
        #     db.session.add(uploads)
        #     db.session.commit()
        #     return response.success({'pathname': renamefile, 'judul': judul}, 'Success upload file!')
        # else:
        #     return response.badRequest([], 'File not allowed!')
    except Exception as e:
        return response.badRequest(e, 'Failed!')
