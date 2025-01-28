from flask import Blueprint, request, jsonify
from app import db, limiter
from models import User
from schemas import user_schema, users_schema
from auth import jwt_required_custom
from utils.security import validate_email

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@limiter.limit("30 per minute")
@jwt_required_custom
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@users_bp.route('/<int:user_id>', methods=['GET'])
@limiter.limit("60 per minute")
@jwt_required_custom
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))

@users_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    data = request.get_json()

    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 201