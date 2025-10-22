"""
Database initialization route for populating training materials on production
"""
from flask import Blueprint, jsonify
from src.models.database import db
from src.models.training_material import TrainingMaterial
import os

init_bp = Blueprint('init', __name__)

@init_bp.route('/api/init-training-materials', methods=['POST'])
def init_training_materials():
    """Initialize training materials in the database"""
    try:
        # Check if materials already exist
        existing = TrainingMaterial.query.first()
        if existing:
            return jsonify({
                'status': 'already_initialized',
                'message': 'Training materials already exist in database'
            }), 200
        
        # Module 1: Sales Mindset & The 10X Rule - One-Page Summary
        material1 = TrainingMaterial(
            module_id=1,
            title="One-Page Summary",
            material_type="summary",
            content="""
            <h2>Module 1: Sales Mindset & The 10X Rule</h2>
            <h3>One-Page Quick Reference</h3>
            
            <div class="section">
                <h4>Core Concept</h4>
                <p>Success in sales isn't about working harder—it's about thinking bigger and taking massive action. Grant Cardone's 10X Rule teaches that extraordinary results require 10 times the effort most people think is necessary. This module establishes the mental foundation for sales excellence.</p>
            </div>
            
            <div class="section">
                <h4>The Four Pillars of Sales Mindset</h4>
                <div class="pillars">
                    <div class="pillar">
                        <h5>1. Abundance Mentality</h5>
                        <p>There are unlimited opportunities. One "no" doesn't matter when there are thousands of potential "yes" responses waiting.</p>
                    </div>
                    <div class="pillar">
                        <h5>2. Massive Action</h5>
                        <p>10X your activity level. If you think you need to make 10 calls, make 100. If you plan 5 meetings, schedule 50.</p>
                    </div>
                    <div class="pillar">
                        <h5>3. Rejection Immunity</h5>
                        <p>Rejection is data, not defeat. Each "no" brings you closer to "yes" and teaches you how to improve your approach.</p>
                    </div>
                    <div class="pillar">
                        <h5>4. Relentless Persistence</h5>
                        <p>Most salespeople quit after 3-5 attempts. Winners keep going. The fortune is in the follow-up.</p>
                    </div>
                </div>
            </div>
            
            <div class="section highlight-yellow">
                <h4>Daily Mindset Routine</h4>
                <ol>
                    <li><strong>Morning Power Hour (6:00-7:00 AM):</strong> Read 30 minutes of sales/mindset content, visualize your goals, review your "why"</li>
                    <li><strong>Pre-Call Ritual:</strong> 3 deep breaths, positive affirmation, review your value proposition</li>
                    <li><strong>Evening Review (9:00 PM):</strong> Journal 3 wins, 1 lesson learned, tomorrow's top 3 priorities</li>
                </ol>
            </div>
            
            <div class="section highlight-green">
                <h4>This Week's Commitment</h4>
                <p><strong>I commit to taking 10X action this week by:</strong></p>
                <ul>
                    <li>Making _____ prospecting calls (10X your normal number)</li>
                    <li>Scheduling _____ discovery meetings</li>
                    <li>Following up with _____ past prospects</li>
                </ul>
                <p><strong>My "Why" (the reason I'm committed to sales excellence):</strong></p>
                <p>_____________________________________________</p>
            </div>
            
            <div class="section highlight-blue">
                <h4>Remember</h4>
                <ul class="checklist">
                    <li>✓ Success is your duty, obligation, and responsibility</li>
                    <li>✓ Average is a failing formula</li>
                    <li>✓ Fear is a sign you're on the right track</li>
                    <li>✓ Massive action cures all fears</li>
                    <li>✓ You can't control outcomes, only activity</li>
                </ul>
            </div>
            """,
            pdf_filename="Module_01_One_Page_Summary.pdf"
        )
        
        # Module 1: Sales Mindset & The 10X Rule - Action Worksheet
        material2 = TrainingMaterial(
            module_id=1,
            title="Action Worksheet",
            material_type="worksheet",
            content="""
            <h2>Module 1: Sales Mindset & The 10X Rule</h2>
            <h3>Action Worksheet</h3>
            
            <div class="section">
                <h4>Part 1: Mindset Self-Assessment</h4>
                <p>Rate yourself honestly on a scale of 1-10:</p>
                <table>
                    <tr>
                        <th>Mindset Element</th>
                        <th>Current Rating</th>
                        <th>Target (End of Week)</th>
                    </tr>
                    <tr>
                        <td>I believe there are unlimited opportunities</td>
                        <td>____/10</td>
                        <td>____/10</td>
                    </tr>
                    <tr>
                        <td>I take massive action consistently</td>
                        <td>____/10</td>
                        <td>____/10</td>
                    </tr>
                    <tr>
                        <td>I handle rejection without emotional impact</td>
                        <td>____/10</td>
                        <td>____/10</td>
                    </tr>
                    <tr>
                        <td>I persist until I achieve my goals</td>
                        <td>____/10</td>
                        <td>____/10</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h4>Part 2: Your 10X Activity Plan</h4>
                <p><strong>Current weekly activity level:</strong></p>
                <ul>
                    <li>Prospecting calls: ______</li>
                    <li>Discovery meetings: ______</li>
                    <li>Follow-up touches: ______</li>
                    <li>Proposals sent: ______</li>
                </ul>
                
                <p><strong>10X weekly activity level (multiply by 10):</strong></p>
                <ul>
                    <li>Prospecting calls: ______</li>
                    <li>Discovery meetings: ______</li>
                    <li>Follow-up touches: ______</li>
                    <li>Proposals sent: ______</li>
                </ul>
            </div>
            
            <div class="section">
                <h4>Part 3: Rejection Reframing Exercise</h4>
                <p>Think of a recent rejection or setback. Reframe it:</p>
                <p><strong>What happened:</strong> _________________________________</p>
                <p><strong>Old interpretation (negative):</strong> _________________________________</p>
                <p><strong>New interpretation (growth-focused):</strong> _________________________________</p>
                <p><strong>What I learned:</strong> _________________________________</p>
                <p><strong>How I'll use this lesson:</strong> _________________________________</p>
            </div>
            
            <div class="section">
                <h4>Part 4: Daily Action Tracker</h4>
                <p>Track your activity for the next 7 days:</p>
                <table>
                    <tr>
                        <th>Day</th>
                        <th>Calls Made</th>
                        <th>Meetings Set</th>
                        <th>Follow-ups</th>
                        <th>Mindset Score (1-10)</th>
                    </tr>
                    <tr><td>Monday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td>Tuesday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td>Wednesday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td>Thursday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td>Friday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td>Saturday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td>Sunday</td><td>____</td><td>____</td><td>____</td><td>____</td></tr>
                    <tr><td><strong>TOTAL</strong></td><td><strong>____</strong></td><td><strong>____</strong></td><td><strong>____</strong></td><td><strong>Avg: ____</strong></td></tr>
                </table>
            </div>
            """,
            pdf_filename="Module_01_Action_Worksheet.pdf"
        )
        
        # Add to database
        db.session.add(material1)
        db.session.add(material2)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Training materials initialized successfully',
            'materials_added': 2
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

