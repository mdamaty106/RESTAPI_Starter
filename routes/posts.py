from flask import Blueprint, request, jsonify
from app import db, limiter
from models import Post
from schemas import post_schema, posts_schema
from auth import jwt_required_custom, get_current_user

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['GET'])
@limiter.limit("100 per minute")
def get_posts():
    posts = Post.query.all()
    return jsonify(posts_schema.dump(posts))

@posts_bp.route('/<int:post_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post_schema.dump(post))

@posts_bp.route('/', methods=['POST'])
@limiter.limit("20 per hour")
@jwt_required_custom
def create_post():
    data = request.get_json()

    if not all(k in data for k in ('title', 'content')):
        return jsonify({'error': 'Missing required fields'}), 400

    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=get_current_user()
    )

    db.session.add(post)
    db.session.commit()

    return jsonify(post_schema.dump(post)), 201

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@limiter.limit("20 per hour")
@jwt_required_custom
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != get_current_user():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']

    db.session.commit()

    return jsonify(post_schema.dump(post))

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@limiter.limit("10 per hour")
@jwt_required_custom
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != get_current_user():
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(post)
    db.session.commit()

    return '', 204