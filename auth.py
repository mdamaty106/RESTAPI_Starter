from datetime import datetime, timedelta
from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import (
    verify_jwt_in_request, create_access_token,
    create_refresh_token, get_jwt_identity,
    get_jwt
)
from models import User, RefreshToken
from app import db

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt = get_jwt()
            if jwt.get('type') != 'access':
                return jsonify({"msg": "Only access tokens are allowed"}), 401
            # Check if token is in blacklist
            if 'jti' in jwt and RefreshToken.query.filter_by(token=jwt['jti'], revoked=True).first():
                return jsonify({"msg": "Token has been revoked"}), 401
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"msg": str(e)}), 401
    return wrapper

def get_current_user():
    try:
        return get_jwt_identity()
    except:
        return None

def create_tokens(user_id):
    """Create both access and refresh tokens."""
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    # Store refresh token in database
    expires_delta = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', timedelta(days=30))
    token = RefreshToken(
        token=refresh_token,
        user_id=user_id,
        expires_at=datetime.utcnow() + expires_delta
    )
    db.session.add(token)
    db.session.commit()

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'expires_in': 3600  # 1 hour for access token
    }

def revoke_token(token_jti, user_id):
    """Revoke a refresh token."""
    token = RefreshToken.query.filter_by(token=token_jti, user_id=user_id).first()
    if token:
        token.revoked = True
        db.session.commit()