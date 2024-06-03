from app import app
from wtforms import validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.datastructures import FileStorage

class DataTestStoreRequest(FlaskForm):
    file = FileField('file', validators=[
        FileRequired(message='File is required'),
        FileAllowed(['mp4', 'mkv', 'avi', 'mov', 'webm'], message='Only video files are allowed (format: mp4, mkv, avi, mov, webm)'),
    ])

    def validate_file(form, field):
        if field.data:
            file = field.data
            if isinstance(file, FileStorage):
                # Check file size (10MB = 10 * 1024 * 1024 bytes)
                if file.content_length > app.config['MAX_VIDEO_CONTENT_LENGTH']:
                    raise validators.ValidationError('File size must not exceed 10MB')

    def to_array(self):
        return {field.name: field.data for field in self}
