import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

# Чорний список токенів
blacklist = set()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Реєстрація маршрутів
    from app.routes.auth import auth_bp
    from app.routes.authors import authors_bp
    from app.routes.books import books_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(books_bp)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist

    return app