#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db
from src.models.module_progress import SalespersonStats
from src.main import app

def update_titles():
    with app.app_context():
        # Update Shawn
        shawn = SalespersonStats.query.filter_by(user_email='shawn@vertexfunding.com').first()
        if shawn:
            shawn.name = 'Shawn - Head of Lead Response'
            print(f"✅ Updated: {shawn.name}")
        
        # Update Ronald
        ronald = SalespersonStats.query.filter_by(user_email='ronald@vertexfunding.com').first()
        if ronald:
            ronald.name = 'Ronald - Head of Client Relationships'
            print(f"✅ Updated: {ronald.name}")
        
        # Update Tamara
        tamara = SalespersonStats.query.filter_by(user_email='tamara@vertexfunding.com').first()
        if tamara:
            tamara.name = 'Tamara - Head of Operations'
            print(f"✅ Updated: {tamara.name}")
        
        db.session.commit()
        print("\n✅ All salesperson titles updated successfully!")

if __name__ == '__main__':
    update_titles()
