from wtforms import Form, StringField, PasswordField, validators

class LoginStoreRequest(Form):
    name = StringField('Name', [validators.DataRequired(message='Name is required')])
    email = StringField('Email', [validators.DataRequired(message='Email is required')])
    password = PasswordField('Password', [
        validators.Length(min=8, message='Password must be at least 8 characters'),
        validators.DataRequired(message='Password is required')
    ])
    
    def to_array(self):
        return {field.name: field.data for field in self}

