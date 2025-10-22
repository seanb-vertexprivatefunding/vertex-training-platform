from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class TrainingMaterial(db.Model):
    __tablename__ = 'training_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False)
    material_type = db.Column(db.String(50), nullable=False)  # 'summary', 'worksheet', 'guide'
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)  # JSON string containing structured content
    pdf_filename = db.Column(db.String(200))  # Reference to existing PDF
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_number': self.module_number,
            'material_type': self.material_type,
            'title': self.title,
            'subtitle': self.subtitle,
            'content': self.content,
            'pdf_filename': self.pdf_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

