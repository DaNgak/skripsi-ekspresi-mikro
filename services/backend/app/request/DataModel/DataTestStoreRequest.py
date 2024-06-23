from app import app
from wtforms import validators, BooleanField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.datastructures import FileStorage

class DataTestStoreRequest(FlaskForm):
    file = FileField('file', validators=[
        FileRequired(message='File is required'),
        FileAllowed(['mp4', 'mkv', 'avi', 'mov', 'webm'], message='Only video files are allowed (format: mp4, mkv, avi, mov, webm)'),
    ])
    with_preview = BooleanField('with_preview', default=False)

    def validate_file(form, field):
        if field.data:
            file = field.data
            if isinstance(file, FileStorage):
                # Check file size (10MB = 10 * 1024 * 1024 bytes)
                if file.content_length > app.config['MAX_VIDEO_CONTENT_LENGTH']:
                    raise validators.ValidationError('File size must not exceed 10MB')

def validate_with_preview(form, field):
    if field.data is not None:
        if isinstance(field.data, bool):
            # No need for conversion if it's already a boolean
            return
        if isinstance(field.data, str):
            # Check if the string is a valid boolean representation
            if field.data.lower() in ['true', 'false']:
                # Convert to boolean
                field.data = field.data.lower() == 'true'
                return
    # If the value is not None, not a boolean, and not a string representation of a boolean, raise an error
    raise validators.ValidationError('Invalid value for with_preview. Must be a boolean.')

    def to_array(self):
        return {field.name: field.data for field in self}
