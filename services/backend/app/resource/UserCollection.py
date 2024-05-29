from app import schema
from app.model.user import User

class UserCollection(schema.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'name', 'email') 