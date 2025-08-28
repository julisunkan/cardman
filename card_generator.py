import os
import uuid
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import zipfile
from datetime import datetime

class CardGenerator:
    def __init__(self):
        self.card_width = 1050  # 3.5 inches at 300 DPI
        self.card_height = 600  # 2 inches at 300 DPI
        self.margin = 60
        
        self.templates = {
            'modern': self.modern_template,
            'classic': self.classic_template,
            'creative': self.creative_template,
            'elegant': self.elegant_template,
            'tech': self.tech_template,
            'corporate': self.corporate_template,
            'artistic': self.artistic_template,
            'minimal': self.minimal_template,
            'bold': self.bold_template,
            'vintage': self.vintage_template,
            'geometric': self.geometric_template,
            'gradient': self.gradient_template,
            'executive': self.executive_template
        }
        
        self.color_schemes = {
            'blue': {'primary': '#2563eb', 'secondary': '#dbeafe', 'text': '#1e293b', 'accent': '#3b82f6'},
            'red': {'primary': '#dc2626', 'secondary': '#fecaca', 'text': '#1e293b', 'accent': '#ef4444'},
            'green': {'primary': '#059669', 'secondary': '#d1fae5', 'text': '#1e293b', 'accent': '#10b981'},
            'purple': {'primary': '#7c3aed', 'secondary': '#e9d5ff', 'text': '#1e293b', 'accent': '#8b5cf6'},
            'orange': {'primary': '#ea580c', 'secondary': '#fed7aa', 'text': '#1e293b', 'accent': '#f97316'},
            'teal': {'primary': '#0d9488', 'secondary': '#ccfbf1', 'text': '#1e293b', 'accent': '#14b8a6'},
            'pink': {'primary': '#db2777', 'secondary': '#fce7f3', 'text': '#1e293b', 'accent': '#ec4899'},
            'indigo': {'primary': '#4338ca', 'secondary': '#e0e7ff', 'text': '#1e293b', 'accent': '#6366f1'},
            'gray': {'primary': '#374151', 'secondary': '#f3f4f6', 'text': '#1e293b', 'accent': '#6b7280'},
            'yellow': {'primary': '#d97706', 'secondary': '#fef3c7', 'text': '#1e293b', 'accent': '#f59e0b'},
            'cyan': {'primary': '#0891b2', 'secondary': '#cffafe', 'text': '#1e293b', 'accent': '#06b6d4'},
            'emerald': {'primary': '#047857', 'secondary': '#d1fae5', 'text': '#1e293b', 'accent': '#059669'},
            'rose': {'primary': '#e11d48', 'secondary': '#ffe4e6', 'text': '#1e293b', 'accent': '#f43f5e'},
            'amber': {'primary': '#d97706', 'secondary': '#fef3c7', 'text': '#1e293b', 'accent': '#f59e0b'},
            'lime': {'primary': '#65a30d', 'secondary': '#ecfccb', 'text': '#1e293b', 'accent': '#84cc16'},
            'black': {'primary': '#000000', 'secondary': '#f8fafc', 'text': '#1e293b', 'accent': '#4b5563'}
        }
        
        self.fonts = {
            'inter': 'Arial',
            'roboto': 'Arial',
            'open_sans': 'Arial',
            'lato': 'Arial',
            'montserrat': 'Arial',
            'poppins': 'Arial',
            'nunito': 'Arial',
            'source_sans': 'Arial',
            'ubuntu': 'Arial',
            'raleway': 'Arial',
            'oswald': 'Arial',
            'merriweather': 'Times New Roman'
        }

    def generate_qr_code(self, card_data):
        """Generate QR code for vCard contact info"""
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{card_data.get('name', '')}
ORG:{card_data.get('company', '')}
TITLE:{card_data.get('job_title', '')}
EMAIL:{card_data.get('email', '')}
TEL:{card_data.get('phone', '')}
URL:{card_data.get('website', '')}
ADR:;;{card_data.get('address', '')};;;;
END:VCARD"""
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(vcard)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        return qr_img

    def get_font_path(self, font_name, size, bold=False):
        """Get system font path - fallback to default fonts"""
        try:
            if bold:
                return ImageFont.truetype("arial.ttf", size)
            else:
                return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

    def modern_template(self, card_data, colors):
        """Modern template with clean lines"""
        img = Image.new('RGB', (self.card_width, self.card_height), colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        # Header bar
        draw.rectangle([0, 0, self.card_width, 120], fill=colors['primary'])
        
        # Name
        name_font = self.get_font_path('inter', 48, bold=True)
        draw.text((self.margin, 40), card_data.get('name', ''), fill='white', font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 24)
        draw.text((self.margin, 160), card_data.get('job_title', ''), fill=colors['text'], font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 20)
        draw.text((self.margin, 200), card_data.get('company', ''), fill=colors['accent'], font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 18)
        y_pos = 260
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 30
        
        return img

    def classic_template(self, card_data, colors):
        """Classic professional template"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([20, 20, self.card_width-20, self.card_height-20], outline=colors['primary'], width=3)
        
        # Name
        name_font = self.get_font_path('inter', 44, bold=True)
        draw.text((self.margin, 80), card_data.get('name', ''), fill=colors['primary'], font=name_font)
        
        # Divider line
        draw.line([self.margin, 140, self.card_width-self.margin, 140], fill=colors['accent'], width=2)
        
        # Job title and company
        title_font = self.get_font_path('inter', 24)
        draw.text((self.margin, 170), card_data.get('job_title', ''), fill=colors['text'], font=title_font)
        draw.text((self.margin, 200), card_data.get('company', ''), fill=colors['accent'], font=title_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 18)
        y_pos = 260
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 30
        
        return img

    def creative_template(self, card_data, colors):
        """Creative template with geometric shapes"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Background shapes
        draw.ellipse([self.card_width-200, -50, self.card_width+50, 200], fill=colors['secondary'])
        draw.rectangle([0, self.card_height-80, 300, self.card_height], fill=colors['primary'])
        
        # Name
        name_font = self.get_font_path('inter', 42, bold=True)
        draw.text((self.margin, 60), card_data.get('name', ''), fill=colors['primary'], font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 22)
        draw.text((self.margin, 120), card_data.get('job_title', ''), fill=colors['text'], font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 20)
        draw.text((self.margin, 150), card_data.get('company', ''), fill=colors['accent'], font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 16)
        y_pos = 200
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 25
        
        return img

    def elegant_template(self, card_data, colors):
        """Elegant template with sophisticated styling"""
        img = Image.new('RGB', (self.card_width, self.card_height), colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        # Elegant border
        draw.rectangle([30, 30, self.card_width-30, self.card_height-30], outline=colors['accent'], width=1)
        draw.rectangle([35, 35, self.card_width-35, self.card_height-35], outline=colors['primary'], width=2)
        
        # Name with elegant styling
        name_font = self.get_font_path('inter', 40, bold=True)
        draw.text((self.margin, 90), card_data.get('name', ''), fill=colors['primary'], font=name_font)
        
        # Decorative line
        draw.line([self.margin, 150, self.card_width//2, 150], fill=colors['accent'], width=1)
        
        # Job title and company
        title_font = self.get_font_path('inter', 22)
        draw.text((self.margin, 180), card_data.get('job_title', ''), fill=colors['text'], font=title_font)
        draw.text((self.margin, 210), card_data.get('company', ''), fill=colors['accent'], font=title_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 16)
        y_pos = 270
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 25
        
        return img

    def tech_template(self, card_data, colors):
        """Tech-inspired template"""
        img = Image.new('RGB', (self.card_width, self.card_height), '#000000')
        draw = ImageDraw.Draw(img)
        
        # Tech grid pattern
        for i in range(0, self.card_width, 50):
            draw.line([i, 0, i, self.card_height], fill='#333333', width=1)
        for i in range(0, self.card_height, 50):
            draw.line([0, i, self.card_width, i], fill='#333333', width=1)
        
        # Accent rectangle
        draw.rectangle([0, 0, 300, self.card_height], fill=colors['primary'])
        
        # Name
        name_font = self.get_font_path('inter', 38, bold=True)
        draw.text((self.margin, 80), card_data.get('name', ''), fill='white', font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 20)
        draw.text((self.margin, 130), card_data.get('job_title', ''), fill=colors['secondary'], font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 18)
        draw.text((self.margin, 160), card_data.get('company', ''), fill='white', font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 16)
        y_pos = 220
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['secondary'], font=contact_font)
                y_pos += 25
        
        return img

    def corporate_template(self, card_data, colors):
        """Corporate professional template"""
        return self.classic_template(card_data, colors)  # Similar to classic

    def artistic_template(self, card_data, colors):
        """Artistic template with creative elements"""
        return self.creative_template(card_data, colors)  # Similar to creative

    def minimal_template(self, card_data, colors):
        """Minimal clean template"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Name
        name_font = self.get_font_path('inter', 46, bold=True)
        draw.text((self.margin, 100), card_data.get('name', ''), fill=colors['text'], font=name_font)
        
        # Simple line
        draw.line([self.margin, 160, self.margin + 200, 160], fill=colors['primary'], width=2)
        
        # Job title
        title_font = self.get_font_path('inter', 24)
        draw.text((self.margin, 190), card_data.get('job_title', ''), fill=colors['accent'], font=title_font)
        
        # Contact info with minimal styling
        contact_font = self.get_font_path('inter', 18)
        y_pos = 250
        for field in ['email', 'phone']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 30
        
        return img

    def bold_template(self, card_data, colors):
        """Bold impactful template"""
        img = Image.new('RGB', (self.card_width, self.card_height), colors['primary'])
        draw = ImageDraw.Draw(img)
        
        # Bold design elements
        draw.rectangle([0, 0, self.card_width, 150], fill=colors['text'])
        
        # Name in bold
        name_font = self.get_font_path('inter', 50, bold=True)
        draw.text((self.margin, 50), card_data.get('name', ''), fill='white', font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 26, bold=True)
        draw.text((self.margin, 180), card_data.get('job_title', ''), fill='white', font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 22)
        draw.text((self.margin, 220), card_data.get('company', ''), fill=colors['secondary'], font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 18, bold=True)
        y_pos = 280
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill='white', font=contact_font)
                y_pos += 30
        
        return img

    def vintage_template(self, card_data, colors):
        """Vintage-style template"""
        img = Image.new('RGB', (self.card_width, self.card_height), '#f5f5dc')
        draw = ImageDraw.Draw(img)
        
        # Vintage border
        draw.rectangle([40, 40, self.card_width-40, self.card_height-40], outline='#8b4513', width=4)
        draw.rectangle([50, 50, self.card_width-50, self.card_height-50], outline='#d2691e', width=2)
        
        # Name
        name_font = self.get_font_path('inter', 42, bold=True)
        draw.text((self.margin, 90), card_data.get('name', ''), fill='#8b4513', font=name_font)
        
        # Decorative elements
        draw.line([self.margin, 150, self.card_width-self.margin, 150], fill='#d2691e', width=2)
        
        # Job title
        title_font = self.get_font_path('inter', 24)
        draw.text((self.margin, 180), card_data.get('job_title', ''), fill='#654321', font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 20)
        draw.text((self.margin, 210), card_data.get('company', ''), fill='#8b4513', font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 16)
        y_pos = 270
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill='#654321', font=contact_font)
                y_pos += 25
        
        return img

    def geometric_template(self, card_data, colors):
        """Geometric pattern template"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Geometric shapes
        draw.polygon([(0, 0), (200, 0), (100, 100)], fill=colors['primary'])
        draw.polygon([(self.card_width, self.card_height), (self.card_width-200, self.card_height), (self.card_width-100, self.card_height-100)], fill=colors['secondary'])
        
        # Name
        name_font = self.get_font_path('inter', 44, bold=True)
        draw.text((self.margin, 140), card_data.get('name', ''), fill=colors['text'], font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 22)
        draw.text((self.margin, 190), card_data.get('job_title', ''), fill=colors['primary'], font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 20)
        draw.text((self.margin, 220), card_data.get('company', ''), fill=colors['accent'], font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 16)
        y_pos = 280
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 25
        
        return img

    def gradient_template(self, card_data, colors):
        """Gradient background template"""
        # Simplified gradient effect
        img = Image.new('RGB', (self.card_width, self.card_height), colors['primary'])
        draw = ImageDraw.Draw(img)
        
        # Simulate gradient with rectangles
        for i in range(self.card_height):
            alpha = i / self.card_height
            # Simple color interpolation
            draw.line([0, i, self.card_width, i], fill=colors['secondary'])
        
        # Overlay for text readability
        draw.rectangle([0, 0, self.card_width, self.card_height], fill=colors['primary'] + '80')
        
        # Name
        name_font = self.get_font_path('inter', 46, bold=True)
        draw.text((self.margin, 80), card_data.get('name', ''), fill='white', font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 24)
        draw.text((self.margin, 140), card_data.get('job_title', ''), fill='white', font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 20)
        draw.text((self.margin, 170), card_data.get('company', ''), fill=colors['secondary'], font=company_font)
        
        # Contact info
        contact_font = self.get_font_path('inter', 18)
        y_pos = 230
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill='white', font=contact_font)
                y_pos += 30
        
        return img

    def executive_template(self, card_data, colors):
        """Executive professional template"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Executive header
        draw.rectangle([0, 0, self.card_width, 100], fill=colors['primary'])
        draw.rectangle([0, 100, self.card_width, 110], fill=colors['accent'])
        
        # Name
        name_font = self.get_font_path('inter', 40, bold=True)
        draw.text((self.margin, 30), card_data.get('name', ''), fill='white', font=name_font)
        
        # Job title
        title_font = self.get_font_path('inter', 26, bold=True)
        draw.text((self.margin, 140), card_data.get('job_title', ''), fill=colors['primary'], font=title_font)
        
        # Company
        company_font = self.get_font_path('inter', 22)
        draw.text((self.margin, 180), card_data.get('company', ''), fill=colors['text'], font=company_font)
        
        # Professional divider
        draw.line([self.margin, 220, self.card_width-self.margin, 220], fill=colors['accent'], width=2)
        
        # Contact info
        contact_font = self.get_font_path('inter', 18)
        y_pos = 250
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 30
        
        return img

    def generate_card(self, card_data):
        """Generate business card image"""
        template_name = card_data.get('template', 'modern')
        color_scheme = card_data.get('color_scheme', 'blue')
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['blue'])
        template_func = self.templates.get(template_name, self.modern_template)
        
        # Generate base card
        card_img = template_func(card_data, colors)
        
        # Add logo if provided
        if card_data.get('logo_path') and os.path.exists(card_data['logo_path']):
            try:
                logo = Image.open(card_data['logo_path'])
                logo.thumbnail((120, 120), Image.Resampling.LANCZOS)
                
                # Position logo in top-right corner
                logo_x = self.card_width - logo.width - self.margin
                logo_y = self.margin
                
                if logo.mode == 'RGBA':
                    card_img.paste(logo, (logo_x, logo_y), logo)
                else:
                    card_img.paste(logo, (logo_x, logo_y))
            except Exception as e:
                print(f"Error adding logo: {e}")
        
        # Add QR code if requested
        if card_data.get('include_qr'):
            try:
                qr_img = self.generate_qr_code(card_data)
                qr_img = qr_img.resize((100, 100), Image.Resampling.LANCZOS)
                
                # Position QR code in bottom-right corner
                qr_x = self.card_width - qr_img.width - self.margin
                qr_y = self.card_height - qr_img.height - self.margin
                
                card_img.paste(qr_img, (qr_x, qr_y))
            except Exception as e:
                print(f"Error adding QR code: {e}")
        
        return card_img

    def generate_preview_card(self, card_data):
        """Generate preview card (smaller size for web display)"""
        card_img = self.generate_card(card_data)
        
        # Resize for web preview
        preview_size = (525, 300)  # Half size for preview
        card_img.thumbnail(preview_size, Image.Resampling.LANCZOS)
        
        # Save preview
        preview_filename = f"preview_{uuid.uuid4().hex}.png"
        preview_path = os.path.join('static', 'previews')
        os.makedirs(preview_path, exist_ok=True)
        preview_filepath = os.path.join(preview_path, preview_filename)
        card_img.save(preview_filepath)
        
        return f"previews/{preview_filename}"

    def export_png(self, card_data):
        """Export card as high-resolution PNG"""
        card_img = self.generate_card(card_data)
        
        filename = f"business_card_{uuid.uuid4().hex}.png"
        filepath = os.path.join('exports', filename)
        card_img.save(filepath, 'PNG', dpi=(300, 300))
        
        return filepath

    def export_pdf(self, card_data):
        """Export card as standard PDF"""
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = f"business_card_{uuid.uuid4().hex}.pdf"
        filepath = os.path.join('exports', filename)
        
        # Generate card image first
        card_img = self.generate_card(card_data)
        temp_img_path = os.path.join('exports', f"temp_{uuid.uuid4().hex}.png")
        card_img.save(temp_img_path)
        
        # Create PDF
        c = canvas.Canvas(filepath, pagesize=letter)
        
        # Convert pixels to points (assuming 300 DPI)
        card_width_pts = self.card_width * 72 / 300
        card_height_pts = self.card_height * 72 / 300
        
        # Center the card on the page
        page_width, page_height = letter
        x = (page_width - card_width_pts) / 2
        y = (page_height - card_height_pts) / 2
        
        c.drawImage(temp_img_path, x, y, width=card_width_pts, height=card_height_pts)
        c.save()
        
        # Clean up temp image
        os.remove(temp_img_path)
        
        return filepath

    def export_pdf_print(self, card_data):
        """Export card as print-ready PDF with bleeds"""
        # For simplicity, using same as standard PDF
        # In production, would add proper bleeds and CMYK conversion
        return self.export_pdf(card_data)

    def export_html(self, card_data):
        """Export card as interactive HTML"""
        filename = f"business_card_{uuid.uuid4().hex}.html"
        filepath = os.path.join('exports', filename)
        
        # Generate card image
        card_img = self.generate_card(card_data)
        img_filename = f"card_{uuid.uuid4().hex}.png"
        img_filepath = os.path.join('exports', img_filename)
        card_img.save(img_filepath)
        
        # Create HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Card - {card_data.get('name', '')}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }}
        .card-container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .card-image {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .contact-info {{
            padding: 20px;
        }}
        .contact-item {{
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        .contact-item:hover {{
            background: #e9ecef;
        }}
        .label {{
            font-weight: bold;
            color: #6c757d;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        .value {{
            font-size: 16px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="card-container">
        <img src="{img_filename}" alt="Business Card" class="card-image">
        <div class="contact-info">
            <h2>Contact Information</h2>
"""
        
        # Add contact fields
        contact_fields = [
            ('name', 'Name'),
            ('job_title', 'Job Title'),
            ('company', 'Company'),
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('website', 'Website'),
            ('address', 'Address')
        ]
        
        for field, label in contact_fields:
            if card_data.get(field):
                html_content += f"""
            <div class="contact-item" onclick="copyToClipboard('{card_data[field]}')">
                <div class="label">{label}</div>
                <div class="value">{card_data[field]}</div>
            </div>
"""
        
        # Add social media if provided
        if card_data.get('social_platform') and card_data.get('social_handle'):
            html_content += f"""
            <div class="contact-item">
                <div class="label">{card_data['social_platform']}</div>
                <div class="value">{card_data['social_handle']}</div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('Copied to clipboard: ' + text);
            });
        }
    </script>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath

    def batch_export(self, csv_data, export_format='png'):
        """Export multiple cards from CSV data"""
        zip_filename = f"business_cards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_filepath = os.path.join('exports', zip_filename)
        
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for i, row in enumerate(csv_data):
                # Map CSV columns to card data
                card_data = {
                    'name': row.get('name', ''),
                    'job_title': row.get('job_title', ''),
                    'company': row.get('company', ''),
                    'email': row.get('email', ''),
                    'phone': row.get('phone', ''),
                    'website': row.get('website', ''),
                    'address': row.get('address', ''),
                    'social_platform': row.get('social_platform', ''),
                    'social_handle': row.get('social_handle', ''),
                    'template': row.get('template', 'modern'),
                    'color_scheme': row.get('color_scheme', 'blue'),
                    'font_family': row.get('font_family', 'inter'),
                    'include_qr': row.get('include_qr', '').lower() in ['true', '1', 'yes']
                }
                
                try:
                    if export_format == 'png':
                        file_path = self.export_png(card_data)
                        arcname = f"card_{i+1}_{card_data.get('name', 'unknown').replace(' ', '_')}.png"
                    elif export_format == 'pdf':
                        file_path = self.export_pdf(card_data)
                        arcname = f"card_{i+1}_{card_data.get('name', 'unknown').replace(' ', '_')}.pdf"
                    else:
                        continue
                    
                    zipf.write(file_path, arcname)
                    os.remove(file_path)  # Clean up individual files
                    
                except Exception as e:
                    print(f"Error generating card {i+1}: {e}")
                    continue
        
        return zip_filepath
