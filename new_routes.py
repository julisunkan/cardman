import os
import json
import csv
import zipfile
import time
from io import StringIO
from flask import render_template, request, session, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from app import app
from advanced_card_generator import AdvancedCardGenerator

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('advanced_index.html')

@app.route('/create')
def create():
    # Initialize advanced session data
    if 'card_data' not in session:
        session['card_data'] = {
            'name': '',
            'job_title': '',
            'company': '',
            'email': '',
            'phone': '',
            'website': '',
            'address': '',
            'social_platform': '',
            'social_handle': '',
            'notes': '',
            'template': 'executive_premium',
            'color_scheme': 'executive_navy',
            'font_family': 'sans_modern',
            'text_align': 'left',
            'include_qr': False,
            'logo_path': '',
            'industry': 'business',
            'style_preference': 'professional'
        }
    
    # Get available templates and color schemes
    generator = AdvancedCardGenerator()
    templates = list(generator.templates.keys())
    color_schemes = list(generator.color_schemes.keys())
    
    return render_template('advanced_create.html', 
                         card_data=session['card_data'],
                         templates=templates,
                         color_schemes=color_schemes)

@app.route('/save_card_data', methods=['POST'])
def save_card_data():
    if 'card_data' not in session:
        session['card_data'] = {}
    
    # Update session with all form data including text formatting
    form_fields = [
        'name', 'job_title', 'company', 'email', 'phone', 'website', 'address',
        'social_platform', 'social_handle', 'notes', 'template', 'color_scheme', 
        'font_family', 'text_align', 'industry', 'style_preference',
        # Text formatting options
        'name_size', 'name_font', 'name_align', 'title_size', 'title_font', 'title_align',
        'company_size', 'company_font', 'company_align', 'contact_size', 'contact_font', 'contact_align'
    ]
    
    # Handle numeric fields
    numeric_fields = ['name_size', 'title_size', 'company_size', 'contact_size']
    
    for field in form_fields:
        if field in numeric_fields:
            try:
                session['card_data'][field] = int(request.form.get(field, 0))
            except (ValueError, TypeError):
                session['card_data'][field] = {
                    'name_size': 72, 'title_size': 32, 'company_size': 28, 'contact_size': 24
                }.get(field, 24)
        else:
            session['card_data'][field] = request.form.get(field, '')
    
    # Handle boolean checkboxes for text formatting
    boolean_fields = ['name_bold', 'name_italic', 'title_bold', 'title_italic', 'company_bold', 'company_italic']
    for field in boolean_fields:
        session['card_data'][field] = field in request.form
    
    for field in form_fields:
        session['card_data'][field] = request.form.get(field, '')
    
    session['card_data']['include_qr'] = 'include_qr' in request.form
    
    # Handle logo upload with enhanced validation
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename and allowed_file(file.filename):
            # Enhanced security and processing
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            try:
                file.save(filepath)
                # Validate image file
                from PIL import Image
                with Image.open(filepath) as img:
                    img.verify()  # Verify it's a valid image
                session['card_data']['logo_path'] = filepath
            except Exception as e:
                flash(f'Invalid image file: {str(e)}', 'error')
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    session.modified = True
    return redirect(url_for('preview'))

@app.route('/preview')
def preview():
    if 'card_data' not in session:
        return redirect(url_for('create'))
    
    card_data = session['card_data']
    generator = AdvancedCardGenerator()
    
    # Generate advanced preview
    try:
        preview_path = generator.generate_preview_card(card_data)
        
        # Get template and color scheme info for display
        template_name = card_data.get('template', 'executive_premium')
        color_scheme = card_data.get('color_scheme', 'executive_navy')
        
        template_info = {
            'executive_premium': 'Executive Premium - Ultra-professional with metallic accents',
            'modern_gradient': 'Modern Gradient - Contemporary with advanced effects',
            'minimalist_pro': 'Minimalist Professional - Clean and sophisticated',
            'creative_artistic': 'Creative Artistic - Bold and innovative',
            'luxury_foil': 'Luxury Foil - Premium with gold elements',
            'tech_neon': 'Tech Neon - Modern technology focused',
            'vintage_letterpress': 'Vintage Letterpress - Classic elegance',
            'geometric_modern': 'Geometric Modern - Contemporary shapes',
            'photography_showcase': 'Photography Showcase - Visual portfolio',
            'corporate_elite': 'Corporate Elite - Business authority',
            'startup_dynamic': 'Startup Dynamic - Innovation focused',
            'healthcare_clean': 'Healthcare Clean - Medical professional',
            'legal_traditional': 'Legal Traditional - Law firm prestige',
            'real_estate_luxury': 'Real Estate Luxury - Property professional',
            'restaurant_elegant': 'Restaurant Elegant - Hospitality focused'
        }
        
        return render_template('advanced_preview.html', 
                             card_data=card_data, 
                             preview_path=preview_path,
                             template_info=template_info.get(template_name, 'Professional Design'))
                             
    except Exception as e:
        flash(f'Error generating preview: {str(e)}', 'error')
        return redirect(url_for('create'))

@app.route('/export/<format>')
def export_card(format):
    if 'card_data' not in session:
        return redirect(url_for('create'))
    
    card_data = session['card_data']
    generator = AdvancedCardGenerator()
    
    try:
        # Ensure exports directory exists
        os.makedirs('exports', exist_ok=True)
        
        if format == 'png_hd':
            file_path = generator.export_png_hd(card_data)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, 
                               download_name='business_card_hd.png',
                               mimetype='image/png')
            else:
                flash('Error: Export file not found', 'error')
                return redirect(url_for('preview'))
                
        elif format == 'pdf_premium':
            file_path = generator.export_premium_pdf(card_data)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, 
                               download_name='business_card_premium.pdf',
                               mimetype='application/pdf')
            else:
                flash('Error: Export file not found', 'error')
                return redirect(url_for('preview'))
                
        elif format == 'pdf_print':
            file_path = generator.export_premium_pdf(card_data, print_ready=True)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, 
                               download_name='business_card_print_ready.pdf',
                               mimetype='application/pdf')
            else:
                flash('Error: Export file not found', 'error')
                return redirect(url_for('preview'))
        else:
            flash('Invalid export format', 'error')
            return redirect(url_for('preview'))
            
    except Exception as e:
        import traceback
        error_msg = f'Error exporting card: {str(e)}'
        print(f"Export error: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        flash(error_msg, 'error')
        return redirect(url_for('preview'))

@app.route('/batch')
def batch():
    # Get available options for batch processing
    generator = AdvancedCardGenerator()
    templates = list(generator.templates.keys())
    color_schemes = list(generator.color_schemes.keys())
    
    return render_template('advanced_batch.html', 
                         templates=templates, 
                         color_schemes=color_schemes)

@app.route('/batch_process', methods=['POST'])
def batch_process():
    if 'csv_file' not in request.files:
        flash('No CSV file uploaded', 'error')
        return redirect(url_for('batch'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('batch'))
    
    if not file.filename or not file.filename.endswith('.csv'):
        flash('Please upload a CSV file', 'error')
        return redirect(url_for('batch'))
    
    try:
        # Read and validate CSV
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        # Validate required columns
        required_columns = ['name', 'job_title', 'company', 'email']
        missing_columns = [col for col in required_columns if col not in csv_reader.fieldnames]
        
        if missing_columns:
            flash(f'CSV missing required columns: {", ".join(missing_columns)}', 'error')
            return redirect(url_for('batch'))
        
        # Process batch with advanced features
        generator = AdvancedCardGenerator()
        export_format = request.form.get('export_format', 'png')
        
        zip_path = generator.batch_export_premium(csv_reader, export_format)
        
        return send_file(zip_path, as_attachment=True, 
                        download_name='premium_business_cards.zip')
    
    except Exception as e:
        flash(f'Error processing batch: {str(e)}', 'error')
        return redirect(url_for('batch'))

@app.route('/templates')
def templates():
    """Template gallery and customization"""
    generator = AdvancedCardGenerator()
    
    template_gallery = {
        'executive_premium': {
            'name': 'Executive Premium',
            'description': 'Ultra-professional design with metallic accents and sophisticated typography',
            'best_for': 'C-level executives, senior management, luxury brands',
            'features': ['Metallic gradients', 'Embossed effects', 'Premium typography']
        },
        'modern_gradient': {
            'name': 'Modern Gradient',
            'description': 'Contemporary design with advanced gradient effects and glassmorphism',
            'best_for': 'Tech companies, startups, creative agencies',
            'features': ['Diagonal gradients', 'Glassmorphism', 'Modern typography']
        },
        'minimalist_pro': {
            'name': 'Minimalist Professional',
            'description': 'Clean, sophisticated design focused on typography and whitespace',
            'best_for': 'Consultants, architects, designers',
            'features': ['Clean typography', 'Minimal design', 'Perfect spacing']
        }
        # Add more template descriptions as needed
    }
    
    return render_template('template_gallery.html', 
                         templates=template_gallery,
                         color_schemes=generator.color_schemes)

@app.route('/api/preview_template', methods=['POST'])
def preview_template():
    """API endpoint for live template preview"""
    try:
        data = request.get_json()
        
        # Create temporary card data for preview
        temp_card_data = {
            'name': data.get('name', 'John Smith'),
            'job_title': data.get('job_title', 'Chief Executive Officer'),
            'company': data.get('company', 'ACME Corporation'),
            'email': data.get('email', 'john.smith@acme.com'),
            'phone': data.get('phone', '+1 (555) 123-4567'),
            'website': data.get('website', 'www.acme.com'),
            'template': data.get('template', 'executive_premium'),
            'color_scheme': data.get('color_scheme', 'executive_navy'),
            'include_qr': data.get('include_qr', False)
        }
        
        generator = AdvancedCardGenerator()
        preview_path = generator.generate_preview_card(temp_card_data)
        
        return jsonify({
            'success': True,
            'preview_url': url_for('static', filename=preview_path.replace('static/', ''))
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash('File too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('create'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500