import os
import logging
from flask import Flask

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'

# Ensure upload and export directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
os.makedirs('static/previews', exist_ok=True)

# Import cleanup service and start it
from cleanup_task import init_cleanup_service
init_cleanup_service()

# Import routes after app creation
import routes

if __name__ == '__main__':
    # This is for local development only - in production, gunicorn handles the server
    app.run(host='0.0.0.0', port=5000, debug=True)
