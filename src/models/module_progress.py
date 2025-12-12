from src.models.user import db
from datetime import datetime

class ModuleProgress(db.Model):
    __tablename__ = 'module_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False, index=True)
    module_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='not_started')  # 'not_started', 'in_progress', 'completed'
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Stats fields
    total_calls = db.Column(db.Integer, default=0)
    total_meetings = db.Column(db.Integer, default=0)
    closed_deals = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_email': self.user_email,
            'module_number': self.module_number,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_calls': self.total_calls,
            'total_meetings': self.total_meetings,
            'closed_deals': self.closed_deals,
            'total_revenue': self.total_revenue,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SalespersonStats(db.Model):
    __tablename__ = 'salesperson_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200))  # Store hashed password
    role = db.Column(db.String(20), default='salesperson')  # 'salesperson' or 'trainer'
    
    # Overall stats
    total_calls = db.Column(db.Integer, default=0)
    total_meetings = db.Column(db.Integer, default=0)
    closed_deals = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0.0)
    
    # Revenue breakdown
    revenue_month = db.Column(db.Float, default=0.0)
    revenue_quarter = db.Column(db.Float, default=0.0)
    revenue_ytd = db.Column(db.Float, default=0.0)
    
    # Current progress
    current_module = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_email': self.user_email,
            'name': self.name,
            'total_calls': self.total_calls,
            'total_meetings': self.total_meetings,
            'closed_deals': self.closed_deals,
            'total_revenue': self.total_revenue,
            'revenue_month': self.revenue_month,
            'revenue_quarter': self.revenue_quarter,
            'revenue_ytd': self.revenue_ytd,
            'current_module': self.current_module,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    module_number = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_email': self.user_email,
            'title': self.title,
            'date': self.date.isoformat() if self.date else None,
            'notes': self.notes,
            'module_number': self.module_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
