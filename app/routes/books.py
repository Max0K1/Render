from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Book, Author

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/", methods=["GET"])
@jwt_required()
def list_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author_id": book.author_id} for book in books])

@books_bp.route("/", methods=["POST"])
@jwt_required()
def create_book():
    data = request.get_json()
    if not data or "title" not in data or "author_id" not in data:
        return {"message": "Invalid data, 'title' and 'author_id' are required"}, 400

    author = Author.query.get(data["author_id"])
    if not author:
        return {"message": f"Author with ID {data['author_id']} not found."}, 404

    new_book = Book(title=data["title"], author=author)
    db.session.add(new_book)
    db.session.commit()
    return {"message": f"Book '{data['title']}' created successfully."}, 201