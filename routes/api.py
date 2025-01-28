from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def api_root():
    return jsonify({
        'message': 'Welcome to the API',
        'version': '1.0',
        'endpoints': {
            'users': '/api/users',
            'posts': '/api/posts',
        }
    })
