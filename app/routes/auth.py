from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return {"message": "Invalid data, 'username' and 'password' are required"}, 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or user.password != data["password"]:
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.username)
    return {"access_token": access_token}, 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return {"message": "Invalid data, 'username' and 'password' are required"}, 400

    if User.query.filter_by(username=data["username"]).first():
        return {"message": "User already exists"}, 400

    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return {"message": f"User '{data['username']}' registered successfully."}, 201