import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS
from middleware.error_handler import register_error_handlers

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt_secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    from routes.api import api_bp
    from routes.users import users_bp
    from routes.posts import posts_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')

    # Initialize app context and create database tables
    with app.app_context():
        import models  # noqa: F401
        db.create_all()

    return app