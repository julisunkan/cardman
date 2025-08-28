import os
import uuid
import qrcode
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
import zipfile
from datetime import datetime
import io
import base64

class AdvancedCardGenerator:
    def __init__(self):
        # Professional business card dimensions (3.5" x 2" at 300 DPI)
        self.card_width = 1050   # 3.5 inches at 300 DPI
        self.card_height = 600   # 2 inches at 300 DPI
        self.dpi = 300
        self.bleed = 9  # 3mm bleed for professional printing
        self.safe_zone = 45  # 15mm safe zone from edges
        
        # Advanced template collection
        self.templates = {
            'executive_premium': self.executive_premium_template,
            'modern_gradient': self.modern_gradient_template,
            'minimalist_pro': self.minimalist_pro_template,
            'creative_artistic': self.creative_artistic_template,
            'luxury_foil': self.luxury_foil_template,
            'tech_neon': self.tech_neon_template,
            'vintage_letterpress': self.vintage_letterpress_template,
            'geometric_modern': self.geometric_modern_template,
            'photography_showcase': self.photography_showcase_template,
            'corporate_elite': self.corporate_elite_template,
            'startup_dynamic': self.startup_dynamic_template,
            'healthcare_clean': self.healthcare_clean_template,
            'legal_traditional': self.legal_traditional_template,
            'real_estate_luxury': self.real_estate_luxury_template,
            'restaurant_elegant': self.restaurant_elegant_template
        }
        
        # Professional color palettes with psychological impact
        self.color_schemes = {
            'executive_navy': {
                'primary': '#1a365d', 'secondary': '#f7fafc', 'accent': '#3182ce',
                'text': '#2d3748', 'light': '#e2e8f0', 'dark': '#1a202c',
                'metallic': '#c6a96b', 'highlight': '#4299e1'
            },
            'luxury_gold': {
                'primary': '#744210', 'secondary': '#fffdf7', 'accent': '#d69e2e',
                'text': '#1a202c', 'light': '#faf5e4', 'dark': '#744210',
                'metallic': '#ecc94b', 'highlight': '#f6e05e'
            },
            'tech_cyan': {
                'primary': '#065f46', 'secondary': '#f0fdfa', 'accent': '#0d9488',
                'text': '#1f2937', 'light': '#ccfbf1', 'dark': '#065f46',
                'metallic': '#5eead4', 'highlight': '#2dd4bf'
            },
            'creative_purple': {
                'primary': '#553c9a', 'secondary': '#faf5ff', 'accent': '#805ad5',
                'text': '#2d3748', 'light': '#e9d8fd', 'dark': '#44337a',
                'metallic': '#b794f6', 'highlight': '#9f7aea'
            },
            'medical_blue': {
                'primary': '#2c5282', 'secondary': '#f7fafc', 'accent': '#3182ce',
                'text': '#2d3748', 'light': '#bee3f8', 'dark': '#2a4365',
                'metallic': '#63b3ed', 'highlight': '#4299e1'
            },
            'finance_green': {
                'primary': '#22543d', 'secondary': '#f0fff4', 'accent': '#38a169',
                'text': '#1a202c', 'light': '#c6f6d5', 'dark': '#1a202c',
                'metallic': '#68d391', 'highlight': '#48bb78'
            },
            'law_burgundy': {
                'primary': '#742a2a', 'secondary': '#fffafa', 'accent': '#c53030',
                'text': '#1a202c', 'light': '#fed7d7', 'dark': '#63171b',
                'metallic': '#fc8181', 'highlight': '#f56565'
            },
            'startup_orange': {
                'primary': '#c05621', 'secondary': '#fffaf0', 'accent': '#dd6b20',
                'text': '#1a202c', 'light': '#fbd38d', 'dark': '#9c4221',
                'metallic': '#f6ad55', 'highlight': '#ed8936'
            }
        }
        
        # Typography system with font fallbacks
        self.font_system = {
            'serif_elegant': ['Times New Roman', 'serif'],
            'sans_modern': ['Arial', 'Helvetica', 'sans-serif'],
            'sans_rounded': ['Arial', 'sans-serif'],
            'mono_tech': ['Courier New', 'monospace'],
            'script_luxury': ['Times New Roman', 'serif']  # Fallback for script fonts
        }
        
    def get_professional_font(self, font_family, size, weight='normal'):
        """Get professional font with proper fallbacks"""
        try:
            fonts = self.font_system.get(font_family, self.font_system['sans_modern'])
            
            for font_name in fonts:
                try:
                    if weight == 'bold':
                        return ImageFont.truetype(f"{font_name}-Bold.ttf", size)
                    elif weight == 'light':
                        return ImageFont.truetype(f"{font_name}-Light.ttf", size)
                    else:
                        return ImageFont.truetype(f"{font_name}.ttf", size)
                except:
                    continue
            
            # Ultimate fallback
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()

    def create_gradient(self, width, height, start_color, end_color, direction='horizontal'):
        """Create advanced gradient backgrounds"""
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        
        if direction == 'horizontal':
            for x in range(width):
                ratio = x / width
                r = int(int(start_color[1:3], 16) * (1 - ratio) + int(end_color[1:3], 16) * ratio)
                g = int(int(start_color[3:5], 16) * (1 - ratio) + int(end_color[3:5], 16) * ratio)
                b = int(int(start_color[5:7], 16) * (1 - ratio) + int(end_color[5:7], 16) * ratio)
                color = f'#{r:02x}{g:02x}{b:02x}'
                draw.line([(x, 0), (x, height)], fill=color)
        elif direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(int(start_color[1:3], 16) * (1 - ratio) + int(end_color[1:3], 16) * ratio)
                g = int(int(start_color[3:5], 16) * (1 - ratio) + int(end_color[3:5], 16) * ratio)
                b = int(int(start_color[5:7], 16) * (1 - ratio) + int(end_color[5:7], 16) * ratio)
                color = f'#{r:02x}{g:02x}{b:02x}'
                draw.line([(0, y), (width, y)], fill=color)
        
        return gradient

    def add_shadow_effect(self, img, offset=5, blur_radius=3, shadow_color='#00000040'):
        """Add professional drop shadow"""
        # Create shadow layer
        shadow = Image.new('RGBA', (img.width + offset*2, img.height + offset*2), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw shadow
        shadow_draw.rectangle([offset, offset, img.width + offset, img.height + offset], 
                             fill=shadow_color)
        
        # Apply blur
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Composite with original
        result = Image.new('RGBA', shadow.size, (255, 255, 255, 0))
        result.paste(shadow, (0, 0))
        result.paste(img, (0, 0), img if img.mode == 'RGBA' else None)
        
        return result

    def generate_advanced_qr(self, card_data, size=120):
        """Generate professional QR code with custom styling"""
        # Enhanced vCard format
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{card_data.get('name', '')}
N:{card_data.get('name', '').split()[-1:] + card_data.get('name', '').split()[:-1]}
ORG:{card_data.get('company', '')}
TITLE:{card_data.get('job_title', '')}
EMAIL;TYPE=WORK:{card_data.get('email', '')}
TEL;TYPE=WORK,VOICE:{card_data.get('phone', '')}
URL:{card_data.get('website', '')}
ADR;TYPE=WORK:;;{card_data.get('address', '')};;;;
NOTE:{card_data.get('notes', '')}
END:VCARD"""
        
        # Create QR with enhanced settings
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=1
        )
        qr.add_data(vcard)
        qr.make(fit=True)
        
        # Generate with custom colors
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Resize to exact dimensions
        qr_img = qr_img.resize((size, size), Image.LANCZOS)
        
        return qr_img

    def executive_premium_template(self, card_data, colors):
        """Ultra-premium executive template with sophisticated design"""
        img = Image.new('RGBA', (self.card_width, self.card_height), colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        # Premium metallic accent stripe
        stripe_height = 80
        gradient_stripe = self.create_gradient(self.card_width, stripe_height, 
                                             colors['primary'], colors['metallic'], 'horizontal')
        img.paste(gradient_stripe, (0, 0))
        
        # Executive embossed border effect
        border_width = 3
        for i in range(border_width):
            alpha = int(255 * (1 - i / border_width) * 0.3)
            border_color = colors['dark'] + f'{alpha:02x}'
            draw.rectangle([i, i, self.card_width - i - 1, self.card_height - i - 1], 
                          outline=border_color, width=1)
        
        # Luxury watermark pattern
        pattern_size = 40
        pattern_alpha = 30
        for x in range(0, self.card_width, pattern_size * 2):
            for y in range(stripe_height, self.card_height, pattern_size * 2):
                draw.ellipse([x, y, x + pattern_size//2, y + pattern_size//2], 
                           fill=colors['light'] + f'{pattern_alpha:02x}')
        
        # Executive name with metallic effect
        name_font = self.get_professional_font('serif_elegant', 58, 'bold')
        name_text = card_data.get('name', '').upper()
        name_x, name_y = self.safe_zone, 100
        
        # Metallic text effect
        shadow_offset = 2
        draw.text((name_x + shadow_offset, name_y + shadow_offset), name_text, 
                 fill=colors['dark'], font=name_font)
        draw.text((name_x, name_y), name_text, fill='white', font=name_font)
        
        # Executive title with prestige
        title_font = self.get_professional_font('sans_modern', 26, 'bold')
        title_y = name_y + 70
        draw.text((name_x, title_y), card_data.get('job_title', ''), 
                 fill=colors['primary'], font=title_font)
        
        # Company with authority
        company_font = self.get_professional_font('serif_elegant', 24)
        company_y = title_y + 40
        draw.text((name_x, company_y), card_data.get('company', ''), 
                 fill=colors['text'], font=company_font)
        
        # Professional divider with gradient
        divider_y = company_y + 50
        divider_gradient = self.create_gradient(280, 4, colors['metallic'], colors['accent'])
        img.paste(divider_gradient, (name_x, divider_y))
        
        # Executive contact grid
        contact_font = self.get_professional_font('sans_modern', 20)
        contact_y = divider_y + 25
        
        contacts = [
            ('EMAIL', card_data.get('email', '')),
            ('PHONE', card_data.get('phone', '')),
            ('WEB', card_data.get('website', ''))
        ]
        
        for label, value in contacts:
            if value:
                # Label in small caps
                label_font = self.get_professional_font('sans_modern', 14, 'bold')
                draw.text((name_x, contact_y), label, fill=colors['accent'], font=label_font)
                draw.text((name_x, contact_y + 18), value, fill=colors['text'], font=contact_font)
                contact_y += 50
        
        # Premium QR code if enabled
        if card_data.get('include_qr', False):
            qr_img = self.generate_advanced_qr(card_data, 100)
            qr_x = self.card_width - 140
            qr_y = self.card_height - 140
            
            # QR background with rounded corners
            qr_bg = Image.new('RGBA', (120, 120), colors['light'])
            img.paste(qr_bg, (qr_x - 10, qr_y - 10))
            img.paste(qr_img, (qr_x, qr_y))
        
        return img.convert('RGB')

    def modern_gradient_template(self, card_data, colors):
        """Modern template with advanced gradient effects"""
        # Create base with diagonal gradient
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        
        # Advanced diagonal gradient
        for y in range(self.card_height):
            for x in range(self.card_width):
                # Calculate diagonal position
                diagonal_pos = (x + y) / (self.card_width + self.card_height)
                
                # Interpolate colors
                r1, g1, b1 = tuple(int(colors['primary'][i:i+2], 16) for i in (1, 3, 5))
                r2, g2, b2 = tuple(int(colors['accent'][i:i+2], 16) for i in (1, 3, 5))
                
                r = int(r1 * (1 - diagonal_pos) + r2 * diagonal_pos)
                g = int(g1 * (1 - diagonal_pos) + g2 * diagonal_pos)
                b = int(b1 * (1 - diagonal_pos) + b2 * diagonal_pos)
                
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Glassmorphism effect overlay
        overlay = Image.new('RGBA', (self.card_width, self.card_height), 
                           colors['secondary'] + '80')
        img.paste(overlay, (0, 0), overlay)
        
        # Modern geometric accent
        accent_points = [(0, 0), (300, 0), (200, 150), (0, 150)]
        draw.polygon(accent_points, fill=colors['light'] + '40')
        
        # Typography with modern hierarchy
        name_font = self.get_professional_font('sans_modern', 68, 'bold')
        draw.text((self.safe_zone, 80), card_data.get('name', ''), 
                 fill='white', font=name_font)
        
        # Modern subtitle
        title_font = self.get_professional_font('sans_modern', 28)
        draw.text((self.safe_zone, 160), card_data.get('job_title', ''), 
                 fill='white', font=title_font)
        
        # Company with style
        company_font = self.get_professional_font('sans_modern', 24, 'light')
        draw.text((self.safe_zone, 200), card_data.get('company', ''), 
                 fill=colors['light'], font=company_font)
        
        # Modern contact layout
        contact_font = self.get_professional_font('sans_modern', 22)
        contact_y = 280
        
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                # Modern bullet point
                draw.ellipse([self.safe_zone, contact_y + 8, 
                             self.safe_zone + 8, contact_y + 16], fill='white')
                draw.text((self.safe_zone + 20, contact_y), card_data[field], 
                         fill='white', font=contact_font)
                contact_y += 35
        
        return img

    def minimalist_pro_template(self, card_data, colors):
        """Ultra-minimalist professional design"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Minimal accent element
        accent_size = 6
        accent_x = self.safe_zone
        accent_y = self.safe_zone
        draw.rectangle([accent_x, accent_y, accent_x + 120, accent_y + accent_size], 
                      fill=colors['primary'])
        
        # Perfect typography hierarchy
        name_font = self.get_professional_font('sans_modern', 72, 'light')
        name_y = accent_y + 30
        draw.text((accent_x, name_y), card_data.get('name', ''), 
                 fill=colors['text'], font=name_font)
        
        # Minimal spacing
        title_font = self.get_professional_font('sans_modern', 26)
        title_y = name_y + 90
        draw.text((accent_x, title_y), card_data.get('job_title', ''), 
                 fill=colors['accent'], font=title_font)
        
        # Company
        company_font = self.get_professional_font('sans_modern', 24, 'light')
        company_y = title_y + 40
        draw.text((accent_x, company_y), card_data.get('company', ''), 
                 fill=colors['text'], font=company_font)
        
        # Minimal contact list
        contact_font = self.get_professional_font('sans_modern', 20)
        contact_y = company_y + 80
        
        contacts = [card_data.get('email', ''), card_data.get('phone', ''), 
                   card_data.get('website', '')]
        
        for contact in contacts:
            if contact:
                draw.text((accent_x, contact_y), contact, 
                         fill=colors['text'], font=contact_font)
                contact_y += 30
        
        # Minimal QR if needed
        if card_data.get('include_qr', False):
            qr_img = self.generate_advanced_qr(card_data, 80)
            qr_x = self.card_width - 120
            qr_y = self.card_height - 120
            img.paste(qr_img, (qr_x, qr_y))
        
        return img

    def generate_card(self, card_data):
        """Generate advanced business card"""
        template_name = card_data.get('template', 'executive_premium')
        color_scheme = card_data.get('color_scheme', 'executive_navy')
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['executive_navy'])
        template_func = self.templates.get(template_name, self.executive_premium_template)
        
        # Generate base card
        card_img = template_func(card_data, colors)
        
        # Add logo if provided
        if card_data.get('logo_path') and os.path.exists(card_data['logo_path']):
            try:
                logo = Image.open(card_data['logo_path'])
                logo = logo.convert('RGBA')
                
                # Smart logo positioning and sizing
                max_logo_size = 120
                logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)
                
                # Position based on template
                logo_x = self.card_width - logo.width - self.safe_zone
                logo_y = self.safe_zone
                
                card_img.paste(logo, (logo_x, logo_y), logo)
            except Exception as e:
                print(f"Logo processing error: {e}")
        
        return card_img

    def generate_preview_card(self, card_data):
        """Generate preview with watermark"""
        card_img = self.generate_card(card_data)
        
        # Add preview watermark
        watermark = Image.new('RGBA', card_img.size, (0, 0, 0, 0))
        watermark_draw = ImageDraw.Draw(watermark)
        
        watermark_font = self.get_professional_font('sans_modern', 32)
        watermark_text = "PREVIEW"
        
        # Center watermark
        bbox = watermark_draw.textbbox((0, 0), watermark_text, font=watermark_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        watermark_x = (card_img.width - text_width) // 2
        watermark_y = (card_img.height - text_height) // 2
        
        watermark_draw.text((watermark_x, watermark_y), watermark_text, 
                           fill=(128, 128, 128, 100), font=watermark_font)
        
        # Composite watermark
        result = Image.alpha_composite(card_img.convert('RGBA'), watermark)
        
        # Save preview
        preview_id = str(uuid.uuid4())
        preview_filename = f"preview_{preview_id}.png"
        preview_path = os.path.join('static/previews', preview_filename)
        
        os.makedirs('static/previews', exist_ok=True)
        result.convert('RGB').save(preview_path, 'PNG', quality=95)
        
        return preview_path

    def export_premium_pdf(self, card_data, print_ready=False):
        """Export professional PDF with print specifications"""
        unique_id = str(uuid.uuid4()).replace('-', '')[:12]
        filename = f"business_card_premium_{unique_id}.pdf"
        filepath = os.path.join('exports', filename)
        
        # Generate high-resolution card
        card_img = self.generate_card(card_data)
        
        # Create PDF with proper print settings
        if print_ready:
            # Print-ready: CMYK, bleeds, crop marks
            doc = SimpleDocTemplate(filepath, pagesize=(4*inch, 2.5*inch),
                                  leftMargin=0.25*inch, rightMargin=0.25*inch,
                                  topMargin=0.25*inch, bottomMargin=0.25*inch)
        else:
            # Standard PDF
            doc = SimpleDocTemplate(filepath, pagesize=(3.5*inch, 2*inch),
                                  leftMargin=0, rightMargin=0,
                                  topMargin=0, bottomMargin=0)
        
        # Convert PIL image to ReportLab
        img_buffer = io.BytesIO()
        card_img.save(img_buffer, format='PNG', quality=95, dpi=(300, 300))
        img_buffer.seek(0)
        
        # Create ReportLab image
        rl_img = RLImage(img_buffer, width=3.5*inch, height=2*inch)
        
        # Build PDF
        story = [rl_img]
        doc.build(story)
        
        return filepath

    def export_png_hd(self, card_data):
        """Export high-definition PNG"""
        unique_id = str(uuid.uuid4()).replace('-', '')[:12]
        filename = f"business_card_hd_{unique_id}.png"
        filepath = os.path.join('exports', filename)
        
        # Generate card at 2x resolution for HD quality
        original_width, original_height = self.card_width, self.card_height
        self.card_width *= 2
        self.card_height *= 2
        
        try:
            card_img = self.generate_card(card_data)
            card_img.save(filepath, 'PNG', quality=100, dpi=(600, 600))
        finally:
            # Restore original dimensions
            self.card_width, self.card_height = original_width, original_height
        
        return filepath

    def batch_export_premium(self, csv_data, export_format='png'):
        """Advanced batch processing with professional output"""
        unique_id = str(uuid.uuid4()).replace('-', '')[:8]
        zip_filename = f"premium_business_cards_{unique_id}.zip"
        zip_path = os.path.join('exports', zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, row in enumerate(csv_data):
                try:
                    # Create card data from CSV row
                    card_data = {
                        'name': row.get('name', ''),
                        'job_title': row.get('job_title', ''),
                        'company': row.get('company', ''),
                        'email': row.get('email', ''),
                        'phone': row.get('phone', ''),
                        'website': row.get('website', ''),
                        'address': row.get('address', ''),
                        'template': row.get('template', 'executive_premium'),
                        'color_scheme': row.get('color_scheme', 'executive_navy'),
                        'include_qr': row.get('include_qr', '').lower() == 'true'
                    }
                    
                    # Generate based on format
                    if export_format == 'pdf':
                        file_path = self.export_premium_pdf(card_data)
                    else:
                        file_path = self.export_png_hd(card_data)
                    
                    # Add to zip with proper naming
                    safe_name = card_data['name'].replace(' ', '_').replace('/', '_')
                    zip_filename = f"{safe_name}_{i+1:03d}.{export_format}"
                    zipf.write(file_path, zip_filename)
                    
                    # Clean up individual file
                    os.remove(file_path)
                    
                except Exception as e:
                    print(f"Error processing row {i}: {e}")
                    continue
        
        return zip_path