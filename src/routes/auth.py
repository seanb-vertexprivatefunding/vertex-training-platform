from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress
from werkzeug.security import check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user with email and password
    Returns user data if successful
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    # Find user in database
    user = SalespersonStats.query.filter_by(user_email=email).first()
    
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check password (simple comparison for now, will use hashing in production)
    if user.password != password:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Get user's module progress
    progress = ModuleProgress.query.filter_by(user_email=email).all()
    completed_modules = [p.module_number for p in progress if p.status == 'completed']
    
    # Get activity data (training sessions)
    from src.models.module_progress import TrainingSession
    sessions = TrainingSession.query.filter_by(user_email=email).all()
    activity_data = [s.to_dict() for s in sessions]
    
    # Return user data
    user_data = {
        'id': f'user_{user.id}',
        'email': user.user_email,
        'name': user.name,
        'role': user.role,
        'currentModule': user.current_module,
        'completedModules': completed_modules,
        'activityData': activity_data,
        'stats': {
            'total_calls': user.total_calls,
            'total_meetings': user.total_meetings,
            'closed_deals': user.closed_deals,
            'total_revenue': user.total_revenue,
            'revenue_month': user.revenue_month,
            'revenue_quarter': user.revenue_quarter,
            'revenue_ytd': user.revenue_ytd
        }
    }
    
    return jsonify({
        'success': True,
        'user': user_data
    }), 200


@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """
    Check if user session is valid
    For now, just returns success (session management to be implemented)
    """
    return jsonify({'valid': True}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout user
    """
    return jsonify({'success': True}), 200
