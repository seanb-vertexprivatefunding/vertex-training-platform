from flask import Blueprint, jsonify
from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress
from datetime import datetime

init_team_bp = Blueprint('init_team', __name__)

@init_team_bp.route('/init-all-team', methods=['GET'])
def init_all_team():
    """Initialize all team members - run once after deployment"""
    
    team_members = [
        {
            'email': 'shawn@vertexfunding.com',
            'name': 'Shawn - Head of Lead Response',
            'modules': [1, 4, 5, 6],
            'completed_modules': [],  # Shawn hasn't completed any yet
            'current_module': 1
        },
        {
            'email': 'ronald@vertexfunding.com',
            'name': 'Ronald - Head of Client Relationships',
            'modules': [2, 7, 10, 11],
            'completed_modules': [1, 2],  # Ronald completed Modules 1 & 2
            'current_module': 3
        },
        {
            'email': 'tamara@vertexfunding.com',
            'name': 'Tamara - Head of Operations',
            'modules': [3, 10, 12],
            'completed_modules': [1, 2],  # Tamara completed Modules 1 & 2
            'current_module': 3
        }
    ]
    
    results = []
    
    for member in team_members:
        # Check if already exists
        existing = SalespersonStats.query.filter_by(user_email=member['email']).first()
        
        if existing:
            # Update name and current module
            existing.name = member['name']
            existing.current_module = member['current_module']
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
                current_module=member['current_module']
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
                # Determine status based on completed modules
                if module_num in member['completed_modules']:
                    status = 'completed'
                    completed_at = datetime.utcnow()
                    started_at = datetime.utcnow()
                else:
                    status = 'not_started'
                    completed_at = None
                    started_at = None
                
                progress = ModuleProgress(
                    user_email=member['email'],
                    module_number=module_num,
                    status=status,
                    started_at=started_at,
                    completed_at=completed_at,
                    total_calls=0,
                    total_meetings=0,
                    closed_deals=0,
                    total_revenue=0.0
                )
                db.session.add(progress)
            else:
                # Update existing progress if needed
                if module_num in member['completed_modules'] and existing_progress.status != 'completed':
                    existing_progress.status = 'completed'
                    existing_progress.completed_at = datetime.utcnow()
                    if not existing_progress.started_at:
                        existing_progress.started_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'All team members initialized successfully!',
        'results': results,
        'team': [
            {
                'name': 'Shawn - Head of Lead Response', 
                'assigned_modules': [1, 4, 5, 6],
                'completed': [],
                'current': 1
            },
            {
                'name': 'Ronald - Head of Client Relationships', 
                'assigned_modules': [2, 7, 10, 11],
                'completed': [1, 2],
                'current': 3
            },
            {
                'name': 'Tamara - Head of Operations', 
                'assigned_modules': [3, 10, 12],
                'completed': [1, 2],
                'current': 3
            },
            {
                'name': 'Sean Bristol (CEO)', 
                'assigned_modules': 'All 12',
                'completed': [],
                'current': 1
            }
        ],
        'next_step': 'Refresh the trainer dashboard at https://vertexsalestraining.com/trainer'
    })
