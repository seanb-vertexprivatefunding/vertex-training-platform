from flask import Blueprint, jsonify
from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/init-ceo', methods=['GET'])
def init_ceo():
    """Initialize CEO user account - run once after deployment"""
    
    # Check if user already exists
    existing = SalespersonStats.query.filter_by(user_email='sean.bristol@icloud.com').first()
    
    if existing:
        return jsonify({
            'status': 'already_exists',
            'message': f'User already exists: {existing.name}',
            'email': existing.user_email
        })
    
    # Create CEO salesperson stats
    ceo_stats = SalespersonStats(
        user_email='sean.bristol@icloud.com',
        name='Sean Bristol (CEO)',
        total_calls=0,
        total_meetings=0,
        closed_deals=0,
        total_revenue=0.0,
        revenue_month=0.0,
        revenue_quarter=0.0,
        revenue_ytd=0.0,
        current_module=1
    )
    
    db.session.add(ceo_stats)
    
    # Initialize module progress for all 12 modules
    for module_num in range(1, 13):
        module_progress = ModuleProgress(
            user_email='sean.bristol@icloud.com',
            module_number=module_num,
            status='not_started',
            total_calls=0,
            total_meetings=0,
            closed_deals=0,
            total_revenue=0.0
        )
        db.session.add(module_progress)
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'CEO user created successfully!',
        'name': 'Sean Bristol (CEO)',
        'email': 'sean.bristol@icloud.com',
        'modules_initialized': 12,
        'next_step': 'Visit https://vertexsalestraining.com/salesperson to access your training dashboard'
    })
