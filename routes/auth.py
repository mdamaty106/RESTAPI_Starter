from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db, limiter
from models import User
from auth import create_tokens, revoke_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify(create_tokens(user.id))
    
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@limiter.limit("10 per minute")
def refresh():
    current_user_id = get_jwt_identity()
    return jsonify(create_tokens(current_user_id))

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    user_id = get_jwt_identity()
    revoke_token(jti, user_id)
    return jsonify({'message': 'Successfully logged out'}), 200

@auth_bp.route('/logout-all', methods=['POST'])
@jwt_required()
@limiter.limit("5 per hour")
def logout_all():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    for token in user.refresh_tokens:
        token.revoked = True
    db.session.commit()
    return jsonify({'message': 'Successfully logged out from all devices'}), 200
