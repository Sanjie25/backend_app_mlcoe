from sqlalchemy.orm import load_only
from app.main import ma
from marshmallow import fields, validate, pre_load, post_load
from app.database_models import Data, User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password_hash = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=6)
    )
    created_at = ma.auto_field(dump_only=True)

    @pre_load
    def process_password(self, data, **kwargs):
        if "password" in data:
            data["password"] = data["password"].strip()
        return data


class DataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Data
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True, validate=validate.Length(min=1, max=200))
    body = ma.auto_field(required=True)
    author_id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
    author = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)


class LoginSchema(ma.Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required=True, load_only=True)


data_schema = DataSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
data_schemas = DataSchema(many=True)
login_schema = LoginSchema()
