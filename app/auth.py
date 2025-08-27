from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
from app.main import db
from app.database_models import User
from app.responses import error_response, success_response
from app.schemas import user_schema, login_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data found", 400)

        print(data["email"])
        validated_data = login_schema.load(data)

        if User.query.filter_by(email=validated_data["email"]).first():
            return error_response("User with this email already exists", 409)
        if User.query.filter_by(username=validated_data["username"]).first():
            return error_response("User with this username already exists", 409)

        new_user = User(
            username=validated_data["username"], email=validated_data["email"]
        )

        new_user.set_password(validated_data["password"])

        db.session.add(new_user)

        db.session.commit()

        login_user(new_user)

        return success_response(user_schema.dump(new_user), "User created")
    except ValidationError as err:
        return error_response(f"ValidationError: {err}", 400)
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Registration failed{e}")


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data was found", 400)

        if "email" in data.keys():
            validated_data = login_schema.load(data)
            user = User.query.filter_by(email=validated_data["email"]).first()
        elif "username" in data.keys():
            validated_data = login_schema.load(data)
            user = User.query.filter_by(username=validated_data["username"]).first()
        else:
            return error_response(data="Username and email not found.", status_code=401)

        if user and user.check_password(validated_data["password"]):
            login_user(user, remember=True)
            return success_response(user_schema.dump(user), "Login Successful")

        return error_response("Incorrect password or username.", 401)

    except ValidationError as err:
        return error_response(message=err.messages, status_code=400)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return success_response(None, message="Logout successful", status_code=200)


@auth_bp.route("/check-auth", methods=["GET"])
@login_required
def check_auth():
    return success_response(
        data=user_schema.dump(current_user),
        message="User is authenticated",
        status_code=200,
    )


@auth_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    return success_response(
        data=user_schema.dump(current_user),
        message="Profile retrieved",
        status_code=200,
    )
