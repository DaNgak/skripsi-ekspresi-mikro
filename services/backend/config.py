# import os

# class Config:
#     def __init__(self):
#         self.database = {
#             'HOST': str(os.environ.get('DB_HOST')),
#             'DATABASE': str(os.environ.get('DB_DATABASE')),
#             'USERNAME': str(os.environ.get('DB_USERNAME')),
#             'PASSWORD': str(os.environ.get('DB_PASSWORD')),
#             'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
#                 username=str(os.environ.get('DB_USERNAME')),
#                 password=str(os.environ.get('DB_PASSWORD')),
#                 host=str(os.environ.get('DB_HOST')),
#                 database=str(os.environ.get('DB_DATABASE'))
#             ),
#             'SQLALCHEMY_TRACK_MODIFICATIONS': False,
#             'SQLALCHEMY_RECORD_QUERIES': True
#         }
#         self.auth = {
#             'JWT_SECRET_KEY': str(os.environ.get('JWT_SECRET'))
#         }
#         self.storage = {
#             'UPLOAD_FOLDER': "upload",
#             'MAX_CONTENT_LENGTH': 2 * 1024 * 1024
#         }

#     def init_app(self, app):
#         # Setting up the database configuration
#         app.config['SQLALCHEMY_DATABASE_URI'] = self.database['SQLALCHEMY_DATABASE_URI']
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = self.database['SQLALCHEMY_TRACK_MODIFICATIONS']
#         app.config['SQLALCHEMY_RECORD_QUERIES'] = self.database['SQLALCHEMY_RECORD_QUERIES']
#         # Setting up the JWT configuration
#         app.config['JWT_SECRET_KEY'] = self.auth['JWT_SECRET_KEY']
        
#         # Setting up the storage configuration
#         app.config['UPLOAD_FOLDER'] = self.storage['UPLOAD_FOLDER']
#         app.config['MAX_CONTENT_LENGTH'] = self.storage['MAX_CONTENT_LENGTH']

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}/{database}'.format(
        username=os.environ.get('DB_USERNAME', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        host=os.environ.get('DB_HOST', 'localhost:3306'),
        database=os.environ.get('DB_DATABASE', 'flask-skripsi')
    )

    SECRET_KEY = 'skripsi-app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'xxxxxx')
    UPLOAD_FOLDER = "assets"
    UPLOAD_FOLDER_VIDEO = "video"
    MAX_VIDEO_CONTENT_LENGTH = 10 * 1024 * 1024
    WTF_CSRF_ENABLED=False
