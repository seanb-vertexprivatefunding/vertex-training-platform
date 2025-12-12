from flask import Blueprint, jsonify
from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress

init_team_bp = Blueprint('init_team', __name__)

@init_team_bp.route('/init-all-team', methods=['GET'])
def init_all_team():
    """Initialize all team members - run once after deployment"""
    
    team_members = [
        {
            'email': 'shawn@vertexfunding.com',
            'name': 'Shawn - Head of Lead Response',
            'modules': [1, 4, 5, 6]
        },
        {
            'email': 'ronald@vertexfunding.com',
            'name': 'Ronald - Head of Client Relationships',
            'modules': [2, 7, 10, 11]
        },
        {
            'email': 'tamara@vertexfunding.com',
            'name': 'Tamara - Head of Operations',
            'modules': [3, 10, 12]
        }
    ]
    
    results = []
    
    for member in team_members:
        # Check if already exists
        existing = SalespersonStats.query.filter_by(user_email=member['email']).first()
        
        if existing:
            # Update name
            existing.name = member['name']
            results.append(f"Updated: {member['name']}")
        else:
            # Create new salesperson
            stats = SalespersonStats(
                user_email=member['email'],
                name=member['name'],
                total_calls=0,
                total_meetings=0,
                closed_deals=0,
                total_revenue=0.0,
                revenue_month=0.0,
                revenue_quarter=0.0,
                revenue_ytd=0.0,
                current_module=1
            )
            db.session.add(stats)
            results.append(f"Created: {member['name']}")
        
        # Initialize module progress for all 12 modules
        for module_num in range(1, 13):
            existing_progress = ModuleProgress.query.filter_by(
                user_email=member['email'],
                module_number=module_num
            ).first()
            
            if not existing_progress:
                progress = ModuleProgress(
                    user_email=member['email'],
                    module_number=module_num,
                    status='not_started',
                    total_calls=0,
                    total_meetings=0,
                    closed_deals=0,
                    total_revenue=0.0
                )
                db.session.add(progress)
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'All team members initialized successfully!',
        'results': results,
        'team': [
            {'name': 'Shawn - Head of Lead Response', 'modules': [1, 4, 5, 6]},
            {'name': 'Ronald - Head of Client Relationships', 'modules': [2, 7, 10, 11]},
            {'name': 'Tamara - Head of Operations', 'modules': [3, 10, 12]},
            {'name': 'Sean Bristol (CEO)', 'modules': 'All 12'}
        ],
        'next_step': 'Refresh the trainer dashboard at https://vertexsalestraining.com/trainer'
    })
