from app import ma
from models import User, Post

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()

class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post

    id = ma.auto_field()
    title = ma.auto_field()
    content = ma.auto_field()
    created_at = ma.auto_field()
    user_id = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
