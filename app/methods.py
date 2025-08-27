from flask import Blueprint, request
from app.main import db
from flask_login import current_user, login_required
from app.database_models import Data
from app.responses import error_response, success_response
from app.schemas import data_schema

data_bp = Blueprint("data", __name__, url_prefix="/data")


# Creating a user using schemas and the data base models
@data_bp.route("/create", methods=["POST"])
@login_required
def create_data():
    try:
        # use fields title and body in json request
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        new_data = Data(
            title=data["title"],
            body=data["body"],
            author_id=current_user.id,
        )

        db.session.add(new_data)
        db.session.commit()

        return success_response(data=data_schema.dump(new_data), status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to create data: {e}", 400)


@data_bp.route("/<int:data_id>", methods=["GET"])
def get_data(data_id):
    data = Data.query.get_or_404(data_id)

    return success_response(data=data_schema.dump(data), status_code=200)


@data_bp.route("/all", methods=["GET"])
def get_all_data():
    res_Data = db.session.execute(db.select(Data)).fetchall()
    result = {}
    n = 0

    for data in res_Data:
        result[n] = data_schema.dump(data[0])
        n += 1

    return success_response(data=result, status_code=200)


@data_bp.route("/delete_by_title", methods=["DELETE"])
@login_required
def delete_data_by_title():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        query_data = db.session.execute(
            db.select(Data).filter_by(title=data["title"])
        ).fetchone()

        db.session.delete(query_data[0])
        db.session.commit()

        return success_response(None, "")

    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to delete data: {e}", 500)


@data_bp.route("/<int:data_id>/delete", methods=["DELETE"])
@login_required
def delete_data(data_id):
    data = Data.query.get_or_404(data_id)

    db.session.delete(data)
    db.session.commit()

    return success_response(None, "")


@data_bp.route("/<int:data_id>/edit", methods=["PUT"])
@login_required
def edit_data(data_id):
    try:
        query_data = Data.query.get_or_404(data_id)

        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        if "title" in data:
            query_data.title = data["title"]
        if "body" in data:
            query_data.body = data["body"]

        db.session.commit()

        return success_response(data=data_schema.dump(query_data))

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to edit data", status_code=304)
