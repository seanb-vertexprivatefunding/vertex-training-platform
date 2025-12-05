from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.module_progress import ModuleProgress, SalespersonStats, TrainingSession
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/salesperson/<email>', methods=['GET'])
def get_salesperson_progress(email):
    """Get complete progress data for a salesperson"""
    try:
        # Get or create salesperson stats
        stats = SalespersonStats.query.filter_by(user_email=email).first()
        if not stats:
            # Create default stats for new salesperson
            stats = SalespersonStats(
                user_email=email,
                name=email.split('@')[0].capitalize()
            )
            db.session.add(stats)
            db.session.commit()
        
        # Get module progress
        module_progress = ModuleProgress.query.filter_by(user_email=email).all()
        
        # Create a map of module number to progress
        progress_map = {p.module_number: p for p in module_progress}
        
        # Build module status for all 12 modules
        modules_status = []
        completed_modules = []
        in_progress_modules = []
        
        for module_num in range(1, 13):
            if module_num in progress_map:
                progress = progress_map[module_num]
                modules_status.append({
                    'module_number': module_num,
                    'status': progress.status,
                    'started_at': progress.started_at.isoformat() if progress.started_at else None,
                    'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
                })
                
                if progress.status == 'completed':
                    completed_modules.append(module_num)
                elif progress.status == 'in_progress':
                    in_progress_modules.append(module_num)
            else:
                # Module not started
                modules_status.append({
                    'module_number': module_num,
                    'status': 'not_started',
                    'started_at': None,
                    'completed_at': None
                })
        
        # Get training sessions
        sessions = TrainingSession.query.filter_by(user_email=email).order_by(TrainingSession.date.desc()).all()
        
        # Build response
        response = {
            'name': stats.name,
            'email': stats.user_email,
            'currentModule': stats.current_module,
            'completedModules': completed_modules,
            'inProgressModules': in_progress_modules,
            'modulesStatus': modules_status,
            'totalCalls': stats.total_calls,
            'totalMeetings': stats.total_meetings,
            'closedDeals': stats.closed_deals,
            'totalRevenue': stats.total_revenue,
            'revenueMonth': stats.revenue_month,
            'revenueQuarter': stats.revenue_quarter,
            'revenueYTD': stats.revenue_ytd,
            'sessions': [s.to_dict() for s in sessions]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@progress_bp.route('/salesperson/<email>/module/<int:module_number>', methods=['POST'])
def update_module_progress(email, module_number):
    """Update progress for a specific module"""
    try:
        data = request.json
        status = data.get('status', 'in_progress')
        
        # Get or create progress record
        progress = ModuleProgress.query.filter_by(
            user_email=email,
            module_number=module_number
        ).first()
        
        if not progress:
            progress = ModuleProgress(
                user_email=email,
                module_number=module_number,
                status=status
            )
            db.session.add(progress)
        else:
            progress.status = status
            progress.updated_at = datetime.utcnow()
        
        # Update timestamps
        if status == 'in_progress' and not progress.started_at:
            progress.started_at = datetime.utcnow()
        elif status == 'completed' and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
        
        # Update stats if provided
        if 'stats' in data:
            stats_data = data['stats']
            progress.total_calls = stats_data.get('total_calls', progress.total_calls)
            progress.total_meetings = stats_data.get('total_meetings', progress.total_meetings)
            progress.closed_deals = stats_data.get('closed_deals', progress.closed_deals)
            progress.total_revenue = stats_data.get('total_revenue', progress.total_revenue)
        
        db.session.commit()
        
        return jsonify(progress.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@progress_bp.route('/salesperson/<email>/stats', methods=['PUT'])
def update_salesperson_stats(email):
    """Update overall stats for a salesperson"""
    try:
        data = request.json
        
        # Get or create stats
        stats = SalespersonStats.query.filter_by(user_email=email).first()
        if not stats:
            stats = SalespersonStats(user_email=email)
            db.session.add(stats)
        
        # Update fields
        if 'name' in data:
            stats.name = data['name']
        if 'total_calls' in data:
            stats.total_calls = data['total_calls']
        if 'total_meetings' in data:
            stats.total_meetings = data['total_meetings']
        if 'closed_deals' in data:
            stats.closed_deals = data['closed_deals']
        if 'total_revenue' in data:
            stats.total_revenue = data['total_revenue']
        if 'revenue_month' in data:
            stats.revenue_month = data['revenue_month']
        if 'revenue_quarter' in data:
            stats.revenue_quarter = data['revenue_quarter']
        if 'revenue_ytd' in data:
            stats.revenue_ytd = data['revenue_ytd']
        if 'current_module' in data:
            stats.current_module = data['current_module']
        
        stats.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(stats.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@progress_bp.route('/salesperson/<email>/session', methods=['POST'])
def add_training_session(email):
    """Add a training session record"""
    try:
        data = request.json
        
        session = TrainingSession(
            user_email=email,
            title=data['title'],
            date=datetime.fromisoformat(data['date']) if 'date' in data else datetime.utcnow(),
            notes=data.get('notes', ''),
            module_number=data.get('module_number')
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify(session.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@progress_bp.route('/team/stats', methods=['GET'])
def get_team_stats():
    """Get stats for all team members"""
    try:
        all_stats = SalespersonStats.query.all()
        return jsonify([s.to_dict() for s in all_stats]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
