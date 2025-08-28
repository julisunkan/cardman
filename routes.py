import os
import json
import csv
import zipfile
import qrcode
from io import BytesIO, StringIO
from flask import render_template, request, session, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from app import app
from card_generator import CardGenerator

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    # Initialize session data if not exists
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
            'template': 'modern',
            'color_scheme': 'blue',
            'font_family': 'inter',
            'text_align': 'left',
            'include_qr': False,
            'logo_path': ''
        }
    return render_template('create.html', card_data=session['card_data'])

@app.route('/save_card_data', methods=['POST'])
def save_card_data():
    if 'card_data' not in session:
        session['card_data'] = {}
    
    # Update session with form data
    for key in ['name', 'job_title', 'company', 'email', 'phone', 'website', 'address',
                'social_platform', 'social_handle', 'template', 'color_scheme', 'font_family',
                'text_align']:
        session['card_data'][key] = request.form.get(key, '')
    
    session['card_data']['include_qr'] = 'include_qr' in request.form
    
    # Handle logo upload
    if 'logo' in request.files:
        file = request.files['logo']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            session['card_data']['logo_path'] = filepath
    
    session.modified = True
    return redirect(url_for('preview'))

@app.route('/preview')
def preview():
    if 'card_data' not in session:
        return redirect(url_for('create'))
    
    card_data = session['card_data']
    generator = CardGenerator()
    
    # Generate preview card
    try:
        preview_path = generator.generate_preview_card(card_data)
        return render_template('preview.html', card_data=card_data, preview_path=preview_path)
    except Exception as e:
        flash(f'Error generating preview: {str(e)}', 'error')
        return redirect(url_for('create'))

@app.route('/export/<format>')
def export_card(format):
    if 'card_data' not in session:
        return redirect(url_for('create'))
    
    card_data = session['card_data']
    generator = CardGenerator()
    
    try:
        if format == 'png':
            file_path = generator.export_png(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card.png')
        elif format == 'pdf':
            file_path = generator.export_pdf(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card.pdf')
        elif format == 'pdf_print':
            file_path = generator.export_pdf_print(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card_print.pdf')
        elif format == 'html':
            file_path = generator.export_html(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card.html')
        else:
            flash('Invalid export format', 'error')
            return redirect(url_for('preview'))
    except Exception as e:
        flash(f'Error exporting card: {str(e)}', 'error')
        return redirect(url_for('preview'))

@app.route('/batch')
def batch():
    return render_template('batch.html')

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
        # Read CSV data
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        generator = CardGenerator()
        zip_path = generator.batch_export(csv_reader, request.form.get('export_format', 'png'))
        
        return send_file(zip_path, as_attachment=True, download_name='business_cards.zip')
    
    except Exception as e:
        flash(f'Error processing batch: {str(e)}', 'error')
        return redirect(url_for('batch'))

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
