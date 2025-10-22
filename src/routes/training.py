from flask import Blueprint, jsonify, request, render_template_string, send_file
from src.models.training_material import TrainingMaterial, db
import json
import io
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

training_bp = Blueprint('training', __name__)

# HTML template for training materials
TRAINING_MATERIAL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #1a5f3f 0%, #2d8659 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1a5f3f 0%, #2d8659 100%);
            color: white;
            padding: 40px 40px 30px;
            text-align: center;
        }
        
        .module-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        
        h1 {
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .subtitle {
            font-size: 18px;
            opacity: 0.95;
            font-weight: 400;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 35px;
        }
        
        .section-title {
            font-size: 24px;
            color: #1a5f3f;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #2d8659;
            font-weight: 600;
        }
        
        .section-content {
            font-size: 16px;
            line-height: 1.8;
            color: #444;
        }
        
        .pillars-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .pillar-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            border-left: 4px solid #2d8659;
        }
        
        .pillar-card h3 {
            color: #1a5f3f;
            margin-bottom: 12px;
            font-size: 18px;
        }
        
        .pillar-card p {
            font-size: 15px;
            color: #555;
            line-height: 1.6;
        }
        
        .insights-list {
            list-style: none;
            margin-top: 15px;
        }
        
        .insights-list li {
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #2d8659;
        }
        
        .insights-list strong {
            color: #1a5f3f;
            font-size: 17px;
            display: block;
            margin-bottom: 8px;
        }
        
        .reframe-table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        
        .reframe-table th {
            background: #1a5f3f;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .reframe-table td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .reframe-table tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        .routine-section {
            background: #fff8e1;
            padding: 25px;
            border-radius: 8px;
            margin-top: 20px;
            border: 2px solid #ffd54f;
        }
        
        .routine-section h4 {
            color: #f57c00;
            margin-bottom: 10px;
            font-size: 18px;
        }
        
        .routine-section ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        
        .routine-section li {
            margin-bottom: 8px;
            color: #555;
        }
        
        .commitment-box {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 30px;
            border-radius: 8px;
            margin-top: 20px;
            border: 2px solid #2d8659;
        }
        
        .commitment-box h3 {
            color: #1a5f3f;
            margin-bottom: 15px;
            font-size: 22px;
        }
        
        .commitment-input {
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-top: 10px;
            border: 1px solid #2d8659;
        }
        
        .remember-list {
            background: #e3f2fd;
            padding: 25px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 4px solid #1976d2;
        }
        
        .remember-list h3 {
            color: #1565c0;
            margin-bottom: 15px;
            font-size: 20px;
        }
        
        .remember-list ul {
            list-style: none;
            margin-left: 0;
        }
        
        .remember-list li {
            padding: 8px 0;
            color: #444;
            font-size: 15px;
        }
        
        .remember-list li:before {
            content: "✓ ";
            color: #1976d2;
            font-weight: bold;
            margin-right: 8px;
        }
        
        .action-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            padding: 30px;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #2d8659;
            color: white;
        }
        
        .btn-primary:hover {
            background: #1a5f3f;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(45, 134, 89, 0.3);
        }
        
        .btn-secondary {
            background: white;
            color: #2d8659;
            border: 2px solid #2d8659;
        }
        
        .btn-secondary:hover {
            background: #2d8659;
            color: white;
            transform: translateY(-2px);
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .action-buttons {
                display: none;
            }
            
            .container {
                box-shadow: none;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                border-radius: 0;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            h1 {
                font-size: 24px;
            }
            
            .content {
                padding: 25px 20px;
            }
            
            .pillars-grid {
                grid-template-columns: 1fr;
            }
            
            .action-buttons {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="module-badge">MODULE {{ module_number }}</div>
            <h1>{{ title }}</h1>
            {% if subtitle %}
            <div class="subtitle">{{ subtitle }}</div>
            {% endif %}
        </div>
        
        <div class="content">
            {{ content_html | safe }}
        </div>
        
        <div class="action-buttons">
            <button class="btn btn-primary" onclick="window.print()">🖨️ Print / Save as PDF</button>
            <a href="/api/training/materials/{{ material_id }}/download-pdf" class="btn btn-secondary">📥 Download PDF</a>
            <button class="btn btn-secondary" onclick="window.history.back()">← Back to Module</button>
        </div>
    </div>
</body>
</html>
'''

@training_bp.route('/materials/<int:material_id>', methods=['GET'])
def get_training_material(material_id):
    """Get training material as web page"""
    material = TrainingMaterial.query.get_or_404(material_id)
    
    # Parse content JSON
    try:
        content_data = json.loads(material.content)
    except:
        content_data = {}
    
    # Generate HTML from content
    content_html = generate_content_html(content_data, material.material_type)
    
    return render_template_string(
        TRAINING_MATERIAL_TEMPLATE,
        title=material.title,
        subtitle=material.subtitle,
        module_number=material.module_number,
        content_html=content_html,
        material_id=material_id
    )

@training_bp.route('/materials/<int:material_id>/download-pdf', methods=['GET'])
def download_training_material_pdf(material_id):
    """Generate and download PDF version of training material"""
    material = TrainingMaterial.query.get_or_404(material_id)
    
    # If we have an existing PDF, serve it
    if material.pdf_filename:
        import os
        # Get the absolute path to the project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pdf_path = os.path.join(project_root, 'src', 'static', 'training-materials', material.pdf_filename)
        if os.path.exists(pdf_path):
            return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name=material.pdf_filename)
    
    # Otherwise generate PDF from HTML
    try:
        content_data = json.loads(material.content)
    except:
        content_data = {}
    
    content_html = generate_content_html(content_data, material.material_type)
    
    html_string = render_template_string(
        TRAINING_MATERIAL_TEMPLATE,
        title=material.title,
        subtitle=material.subtitle,
        module_number=material.module_number,
        content_html=content_html,
        material_id=material_id
    )
    
    # Generate PDF
    font_config = FontConfiguration()
    pdf_bytes = HTML(string=html_string).write_pdf(font_config=font_config)
    
    # Create filename
    filename = f"Module_{material.module_number:02d}_{material.material_type}.pdf"
    
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@training_bp.route('/materials', methods=['GET'])
def list_training_materials():
    """List all training materials"""
    module = request.args.get('module', type=int)
    material_type = request.args.get('type')
    
    query = TrainingMaterial.query
    
    if module:
        query = query.filter_by(module_number=module)
    if material_type:
        query = query.filter_by(material_type=material_type)
    
    materials = query.order_by(TrainingMaterial.module_number, TrainingMaterial.material_type).all()
    
    return jsonify([material.to_dict() for material in materials])

def generate_content_html(content_data, material_type):
    """Generate HTML content from structured data"""
    html_parts = []
    
    if material_type == 'summary':
        # Generate One-Page Summary HTML
        if 'core_concept' in content_data:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">Core Concept</h2>
                <div class="section-content">
                    <p>{content_data['core_concept']}</p>
                </div>
            </div>
            ''')
        
        if 'pillars' in content_data:
            html_parts.append('<div class="section"><h2 class="section-title">The Four Pillars</h2>')
            html_parts.append('<div class="pillars-grid">')
            for pillar in content_data['pillars']:
                html_parts.append(f'''
                <div class="pillar-card">
                    <h3>{pillar['title']}</h3>
                    <p>{pillar['description']}</p>
                </div>
                ''')
            html_parts.append('</div></div>')
        
        if 'insights' in content_data:
            html_parts.append('<div class="section"><h2 class="section-title">Key Insights from Top Sales Leaders</h2>')
            html_parts.append('<ul class="insights-list">')
            for insight in content_data['insights']:
                html_parts.append(f'''
                <li>
                    <strong>{insight['leader']}</strong>
                    {insight['quote']}
                </li>
                ''')
            html_parts.append('</ul></div>')
        
        if 'reframes' in content_data:
            html_parts.append('<div class="section"><h2 class="section-title">Reframing Negative Self-Talk</h2>')
            html_parts.append('<table class="reframe-table">')
            html_parts.append('<tr><th>Negative Thought</th><th>Powerful Reframe</th></tr>')
            for reframe in content_data['reframes']:
                html_parts.append(f'''
                <tr>
                    <td>{reframe['negative']}</td>
                    <td>{reframe['positive']}</td>
                </tr>
                ''')
            html_parts.append('</table></div>')
        
        if 'routine' in content_data:
            html_parts.append('<div class="section"><h2 class="section-title">Your Daily Mindset Routine</h2>')
            html_parts.append('<div class="routine-section">')
            for time_block in content_data['routine']:
                html_parts.append(f'<h4>{time_block["time"]}</h4>')
                html_parts.append('<ul>')
                for item in time_block['activities']:
                    html_parts.append(f'<li>{item}</li>')
                html_parts.append('</ul>')
            html_parts.append('</div></div>')
        
        if 'commitment' in content_data:
            html_parts.append(f'''
            <div class="section">
                <div class="commitment-box">
                    <h3>This Week's Commitment</h3>
                    <p>{content_data['commitment']['text']}</p>
                    <div class="commitment-input">
                        <strong>My daily activity target:</strong><br>
                        Prospecting calls/contacts: _____<br>
                        Conversations: _____<br>
                        Meetings scheduled: _____
                    </div>
                </div>
            </div>
            ''')
        
        if 'remember' in content_data:
            html_parts.append('<div class="section"><div class="remember-list"><h3>Remember</h3><ul>')
            for item in content_data['remember']:
                html_parts.append(f'<li>{item}</li>')
            html_parts.append('</ul></div></div>')
    
    return '\n'.join(html_parts)

