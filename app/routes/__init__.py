from .auth import auth_bp
from .authors import authors_bp
from .books import books_bp

# Експортуємо маршрути, щоб їх можна було імпортувати з app.routes
__all__ = ["auth_bp", "authors_bp", "books_bp"]