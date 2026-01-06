#!/usr/bin/env python3
"""
Initialize all team members in the Vertex Sales Training Platform
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db
from src.models.module_progress import SalespersonStats, ModuleProgress
from src.main import app

def initialize_team():
    with app.app_context():
        team_members = [
            {
                'email': 'shawn@vertexfunding.com',
                'name': 'Shawn - Head of Lead Response',
                'modules': [1, 4, 5, 6]  # His assigned modules
            },
            {
                'email': 'ronald@vertexfunding.com',
                'name': 'Ronald - Head of Client Relationships',
                'modules': [2, 7, 10, 11]  # His assigned modules
            },
            {
                'email': 'tamara@vertexfunding.com',
                'name': 'Tamara - Head of Operations',
                'modules': [3, 10, 12]  # Her assigned modules
            }
        ]
        
        for member in team_members:
            # Check if already exists
            existing = SalespersonStats.query.filter_by(user_email=member['email']).first()
            
            if existing:
                # Update name if changed
                existing.name = member['name']
                print(f"✅ Updated: {member['name']} ({member['email']})")
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
                print(f"✅ Created: {member['name']} ({member['email']})")
            
            # Initialize module progress for all 12 modules
            for module_num in range(1, 13):
                existing_progress = ModuleProgress.query.filter_by(
                    user_email=member['email'],
                    module_number=module_num
                ).first()
                
                if not existing_progress:
                    # Determine status based on assigned modules
                    if module_num in member['modules']:
                        status = 'not_started'  # Assigned to them
                    else:
                        status = 'not_started'  # Available but not primary
                    
                    progress = ModuleProgress(
                        user_email=member['email'],
                        module_number=module_num,
                        status=status,
                        total_calls=0,
                        total_meetings=0,
                        closed_deals=0,
                        total_revenue=0.0
                    )
                    db.session.add(progress)
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ ALL TEAM MEMBERS INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\nTeam Members:")
        print("- Shawn (Lead Response) - Modules 1, 4, 5, 6")
        print("- Ronald (Client Relationships) - Modules 2, 7, 10, 11")
        print("- Tamara (Operations) - Modules 3, 10, 12")
        print("- Sean Bristol (CEO) - All 12 modules")
        print("\nRefresh the trainer dashboard to see all team members!")

if __name__ == '__main__':
    initialize_team()
