import os
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from middleware.error_handler import register_error_handlers

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    from routes.api import api_bp
    from routes.users import users_bp
    from routes.posts import posts_bp
    from routes.auth import auth_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Initialize app context and create database tables
    with app.app_context():
        import models  # noqa: F401
        db.create_all()

    return app