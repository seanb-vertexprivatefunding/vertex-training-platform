#!/usr/bin/env python3
"""
Script to add CEO user to the Vertex Sales Training Platform
Run this after deployment to initialize the CEO account
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress
from src.main import app

def add_ceo_user():
    with app.app_context():
        # Check if user already exists
        existing = SalespersonStats.query.filter_by(user_email='sean.bristol@icloud.com').first()
        
        if existing:
            print(f"User already exists: {existing.name} ({existing.user_email})")
            return
        
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
        print("✅ CEO user created successfully!")
        print(f"   Name: Sean Bristol (CEO)")
        print(f"   Email: sean.bristol@icloud.com")
        print(f"   Modules initialized: 1-12")
        print("\nYou can now access the training platform at:")
        print("https://vertexsalestraining.com/salesperson")

if __name__ == '__main__':
    add_ceo_user()
