from flask import Blueprint, jsonify
from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress
from datetime import datetime

init_team_bp = Blueprint('init_team', __name__)

@init_team_bp.route('/init-all-team', methods=['GET'])
def init_all_team():
    """Initialize all team members with passwords - run once after deployment"""
    
    team_members = [
        {
            'email': 'seanb@vertexprivatefunding.com',
            'name': 'Sean B - CEO/Trainer',
            'password': 'trainer123',
            'role': 'trainer',
            'modules': list(range(1, 13)),  # All modules
            'completed_modules': [],
            'current_module': 1
        },
        {
            'email': 'sean.bristol@icloud.com',
            'name': 'Sean Bristol (Personal Training Account)',
            'password': 'vertex2024',
            'role': 'salesperson',
            'modules': list(range(1, 13)),  # All modules for CEO to go through training
            'completed_modules': [],
            'current_module': 1
        },
        {
            'email': 'shawn@vertexprivatefunding.com',
            'name': 'Shawn - Head of Lead Response',
            'password': 'sales123',
            'role': 'salesperson',
            'modules': [1, 4, 5, 6],
            'completed_modules': [],
            'current_module': 1
        },
        {
            'email': 'ronald@vertexprivatefunding.com',
            'name': 'Ronald - Head of Client Relationships',
            'password': 'sales123',
            'role': 'salesperson',
            'modules': [2, 7, 10, 11],
            'completed_modules': [1, 2],
            'current_module': 3
        },
        {
            'email': 'tamara@vertexprivatefunding.com',
            'name': 'Tamara - Head of Operations',
            'password': 'sales123',
            'role': 'salesperson',
            'modules': [3, 10, 12],
            'completed_modules': [1, 2],
            'current_module': 3
        }
    ]
    
    results = []
    
    for member in team_members:
        # Check if already exists
        existing = SalespersonStats.query.filter_by(user_email=member['email']).first()
        
        if existing:
            # Update name, password, role, and current module
            existing.name = member['name']
            existing.password = member['password']
            existing.role = member['role']
            existing.current_module = member['current_module']
            results.append(f"Updated: {member['name']}")
        else:
            # Create new user
            stats = SalespersonStats(
                user_email=member['email'],
                name=member['name'],
                password=member['password'],
                role=member['role'],
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
        'message': 'All team members initialized with authentication!',
        'results': results,
        'credentials': [
            {
                'name': 'Sean B - CEO/Trainer',
                'email': 'seanb@vertexprivatefunding.com',
                'password': 'trainer123',
                'role': 'Trainer (see all salespeople)',
                'access': 'All 12 modules'
            },
            {
                'name': 'Sean Bristol (Personal Training)',
                'email': 'sean.bristol@icloud.com',
                'password': 'vertex2024',
                'role': 'Salesperson (go through training)',
                'access': 'All 12 modules'
            },
            {
                'name': 'Shawn - Lead Response',
                'email': 'shawn@vertexprivatefunding.com',
                'password': 'sales123',
                'role': 'Salesperson',
                'assigned_modules': [1, 4, 5, 6]
            },
            {
                'name': 'Ronald - Client Relationships',
                'email': 'ronald@vertexprivatefunding.com',
                'password': 'sales123',
                'role': 'Salesperson',
                'assigned_modules': [2, 7, 10, 11],
                'completed': [1, 2]
            },
            {
                'name': 'Tamara - Operations',
                'email': 'tamara@vertexprivatefunding.com',
                'password': 'sales123',
                'role': 'Salesperson',
                'assigned_modules': [3, 10, 12],
                'completed': [1, 2]
            }
        ],
        'next_step': 'The frontend will now authenticate via /api/auth/login endpoint'
    })
