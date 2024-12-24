from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Author

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@authors_bp.route("/", methods=["GET"])
@jwt_required()
def list_authors():
    authors = Author.query.all()
    return jsonify([{"id": author.id, "name": author.name} for author in authors])

@authors_bp.route("/", methods=["POST"])
@jwt_required()
def create_author():
    data = request.get_json()
    if not data or "name" not in data:
        return {"message": "Invalid data, 'name' is required"}, 400

    new_author = Author(name=data["name"])
    db.session.add(new_author)
    db.session.commit()
    return {"message": f"Author '{data['name']}' created successfully."}, 201