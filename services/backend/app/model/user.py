from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True )
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def __str__(self):
        return f'{self.name}'   
    
    def setPassword(self, password):
        self.password = generate_password_hash(password=password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)