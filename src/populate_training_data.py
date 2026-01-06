#!/usr/bin/env python3
"""
Script to populate training materials database with content
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.training_material import TrainingMaterial, db
import json

def populate_module_1_summary():
    """Populate Module 1 One-Page Summary"""
    content = {
        "core_concept": "Sales success starts with mindset, not technique. Your beliefs about yourself, your product, and your prospects determine your results more than any script or strategy.",
        "pillars": [
            {
                "title": "1. Abundance Thinking",
                "description": "There are unlimited opportunities. One \"no\" doesn't matter because thousands of potential \"yeses\" exist. Scarcity thinking leads to desperation."
            },
            {
                "title": "2. Massive Action",
                "description": "Success = (Activity × Skill) + Consistency. Take 10X more action than you think is necessary. Action cures fear and builds confidence."
            },
            {
                "title": "3. Resilience & Persistence",
                "description": "Bounce back quickly from rejection. Use the 5-Minute Rule: Feel disappointed for 5 minutes, then move to the next opportunity."
            },
            {
                "title": "4. Continuous Improvement",
                "description": "Every interaction is a learning opportunity. Study, practice, and refine your approach daily."
            }
        ],
        "insights": [
            {
                "leader": "Grant Cardone - The 10X Rule",
                "quote": "Whatever level of effort you think is required, multiply it by 10. Most people drastically underestimate the action needed for success."
            },
            {
                "leader": "Zig Ziglar - Transfer of Belief",
                "quote": "\"Sales is a transfer of feeling. The prospect must feel your conviction before they'll buy your product.\""
            },
            {
                "leader": "Jeb Blount - Fanatical Prospecting",
                "quote": "\"The pipeline is the lifeblood of sales. Massive, consistent prospecting activity is non-negotiable for success.\""
            }
        ],
        "reframes": [
            {
                "negative": "I'm bothering people",
                "positive": "I'm offering solutions to real problems"
            },
            {
                "negative": "I'm not good at sales",
                "positive": "I'm developing my sales skills every day"
            },
            {
                "negative": "People don't want to hear from me",
                "positive": "The right people are waiting for my solution"
            },
            {
                "negative": "I hate rejection",
                "positive": "Every no brings me closer to a yes"
            }
        ],
        "routine": [
            {
                "time": "Morning (10 minutes)",
                "activities": [
                    "Read your commitment declaration out loud",
                    "Visualize 3 successful sales conversations",
                    "Review your activity goals for the day"
                ]
            },
            {
                "time": "During the Day",
                "activities": [
                    "Apply the 5-Minute Rule after any rejection",
                    "Track your activity numbers in real-time",
                    "Celebrate small wins immediately"
                ]
            },
            {
                "time": "Evening (10 minutes)",
                "activities": [
                    "Write down 3 wins from today (no matter how small)",
                    "Journal one lesson learned",
                    "Prepare tomorrow's prospecting list"
                ]
            }
        ],
        "commitment": {
            "text": "I commit to taking massive action by setting and achieving my daily activity targets."
        },
        "remember": [
            "Sales is a skill that can be learned and mastered",
            "Rejection is normal and necessary for success",
            "Massive action creates momentum and confidence",
            "Your mindset determines your results",
            "Every top performer started where you are now"
        ]
    }
    
    material = TrainingMaterial(
        module_number=1,
        material_type='summary',
        title='Sales Mindset & The 10X Rule',
        subtitle='One-Page Quick Reference',
        content=json.dumps(content),
        pdf_filename='Module_01_One_Page_Summary.pdf'
    )
    
    return material

def populate_module_1_worksheet():
    """Populate Module 1 Action Worksheet"""
    content = {
        "sections": [
            {
                "title": "Part 1: Your Current Sales Mindset Assessment",
                "questions": [
                    "On a scale of 1-10, how would you rate your current sales confidence?",
                    "What negative thoughts come up most often when prospecting or closing?",
                    "How do you typically respond to rejection? (Describe your emotional and behavioral response)",
                    "What beliefs about sales or selling might be holding you back?"
                ]
            },
            {
                "title": "Part 2: The 10X Action Plan",
                "instructions": "For each activity below, write what you THINK you should do, then multiply by 10:",
                "activities": [
                    "Prospecting calls per day",
                    "Follow-up emails per week",
                    "Networking conversations per week",
                    "Hours spent on sales activities per day"
                ]
            },
            {
                "title": "Part 3: Reframing Exercise",
                "instructions": "Write your most common negative sales thoughts, then create powerful reframes:",
                "examples": [
                    "My Negative Thought: _______________",
                    "Powerful Reframe: _______________"
                ]
            },
            {
                "title": "Part 4: Your Personal Commitment Declaration",
                "instructions": "Complete this declaration and read it aloud every morning:",
                "template": [
                    "I am committed to becoming a top-performing sales professional.",
                    "I will take massive action every single day.",
                    "I embrace rejection as part of my path to success.",
                    "I will make [NUMBER] prospecting calls every day.",
                    "I will schedule [NUMBER] meetings every week.",
                    "I will close [NUMBER] deals this month.",
                    "Nothing will stop me from achieving my goals."
                ]
            },
            {
                "title": "Part 5: This Week's Action Commitment",
                "daily_targets": [
                    "Prospecting calls/contacts: _____",
                    "Meaningful conversations: _____",
                    "Meetings scheduled: _____",
                    "Follow-ups completed: _____"
                ]
            }
        ]
    }
    
    material = TrainingMaterial(
        module_number=1,
        material_type='worksheet',
        title='Sales Mindset & The 10X Rule',
        subtitle='Action Worksheet',
        content=json.dumps(content),
        pdf_filename='Module_01_Action_Worksheet.pdf'
    )
    
    return material

def main():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        existing = TrainingMaterial.query.filter_by(module_number=1).first()
        if existing:
            print("Training materials already exist. Skipping population.")
            return
        
        # Add Module 1 materials
        materials = [
            populate_module_1_summary(),
            populate_module_1_worksheet()
        ]
        
        for material in materials:
            db.session.add(material)
        
        db.session.commit()
        print(f"Successfully added {len(materials)} training materials to the database.")
        
        # List all materials
        all_materials = TrainingMaterial.query.all()
        print(f"\nTotal training materials in database: {len(all_materials)}")
        for mat in all_materials:
            print(f"  - Module {mat.module_number}: {mat.title} ({mat.material_type})")

if __name__ == '__main__':
    main()

