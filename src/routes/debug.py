from flask import Blueprint, jsonify
from src.models.module_progress import SalespersonStats

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/list-users', methods=['GET'])
def list_users():
    """List all users in the database for debugging"""
    users = SalespersonStats.query.all()
    
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.user_email,
            'name': user.name,
            'role': user.role,
            'has_password': bool(user.password),
            'password_length': len(user.password) if user.password else 0,
            'current_module': user.current_module
        })
    
    return jsonify({
        'total_users': len(users),
        'users': user_list
    })
