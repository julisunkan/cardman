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
        # Standard business card dimensions at 300 DPI for professional printing
        self.card_width = 1050   # 3.5 inches at 300 DPI
        self.card_height = 600   # 2 inches at 300 DPI
        self.dpi = 300
        self.margin = 45         # Professional margin
        self.safe_margin = 30    # Content safe area
        
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
        
        # Professional color schemes with sophisticated palettes
        self.color_schemes = {
            'corporate_blue': {
                'primary': '#1e3a8a', 'secondary': '#f1f5f9', 'text': '#0f172a', 
                'accent': '#3b82f6', 'light': '#e2e8f0', 'dark': '#334155'
            },
            'executive_navy': {
                'primary': '#1e293b', 'secondary': '#f8fafc', 'text': '#0f172a',
                'accent': '#64748b', 'light': '#e2e8f0', 'dark': '#475569'
            },
            'professional_gray': {
                'primary': '#374151', 'secondary': '#f9fafb', 'text': '#111827',
                'accent': '#6b7280', 'light': '#e5e7eb', 'dark': '#4b5563'
            },
            'modern_black': {
                'primary': '#000000', 'secondary': '#ffffff', 'text': '#000000',
                'accent': '#404040', 'light': '#f5f5f5', 'dark': '#262626'
            },
            'elegant_burgundy': {
                'primary': '#7c2d12', 'secondary': '#fef7f0', 'text': '#1c1917',
                'accent': '#dc2626', 'light': '#fed7d7', 'dark': '#991b1b'
            },
            'sophisticated_green': {
                'primary': '#14532d', 'secondary': '#f0fdf4', 'text': '#052e16',
                'accent': '#16a34a', 'light': '#dcfce7', 'dark': '#166534'
            },
            'premium_gold': {
                'primary': '#92400e', 'secondary': '#fffbeb', 'text': '#451a03',
                'accent': '#d97706', 'light': '#fef3c7', 'dark': '#a16207'
            },
            'royal_purple': {
                'primary': '#581c87', 'secondary': '#faf5ff', 'text': '#2e1065',
                'accent': '#8b5cf6', 'light': '#e9d5ff', 'dark': '#6d28d9'
            }
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

    def get_font_path(self, font_name, size, bold=False, style='normal'):
        """Get professional font with proper hierarchy"""
        try:
            # Try to load better fonts for professional appearance
            font_paths = {
                'regular': ['Arial.ttf', 'arial.ttf', 'DejaVuSans.ttf'],
                'bold': ['Arial-Bold.ttf', 'arialbd.ttf', 'DejaVuSans-Bold.ttf'],
                'light': ['Arial.ttf', 'arial.ttf', 'DejaVuSans.ttf']
            }
            
            target_style = 'bold' if bold else 'regular'
            
            for font_path in font_paths[target_style]:
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
            
            # Fallback to default
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()

    def modern_template(self, card_data, colors):
        """Ultra-modern professional template with sophisticated layout"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Sophisticated vertical accent bar
        accent_width = 8
        draw.rectangle([0, 0, accent_width, self.card_height], fill=colors['primary'])
        
        # Subtle background pattern
        bg_rect = Image.new('RGBA', (self.card_width - accent_width, self.card_height), 
                           colors['light'] + '20')
        img.paste(bg_rect, (accent_width, 0), bg_rect)
        
        # Content area with proper margins
        content_x = accent_width + self.safe_margin
        
        # Name with professional hierarchy
        name_font = self.get_font_path('inter', 48, bold=True)
        name_y = 45
        draw.text((content_x, name_y), card_data.get('name', '').upper(), 
                 fill=colors['primary'], font=name_font)
        
        # Professional divider line
        line_y = name_y + 65
        line_length = 180
        draw.rectangle([content_x, line_y, content_x + line_length, line_y + 2], 
                      fill=colors['accent'])
        
        # Job title with sophisticated spacing
        title_font = self.get_font_path('inter', 22, bold=False)
        title_y = line_y + 20
        draw.text((content_x, title_y), card_data.get('job_title', ''), 
                 fill=colors['text'], font=title_font)
        
        # Company name with emphasis
        company_font = self.get_font_path('inter', 20, bold=True)
        company_y = title_y + 35
        draw.text((content_x, company_y), card_data.get('company', ''), 
                 fill=colors['accent'], font=company_font)
        
        # Contact information with professional formatting
        contact_font = self.get_font_path('inter', 18)
        contact_y = company_y + 60
        
        contact_items = [
            ('email', card_data.get('email', '')),
            ('phone', card_data.get('phone', '')),
            ('website', card_data.get('website', ''))
        ]
        
        for label, value in contact_items:
            if value:
                draw.text((content_x, contact_y), value, fill=colors['text'], font=contact_font)
                contact_y += 30
        
        return img

    def classic_template(self, card_data, colors):
        """Timeless professional template with elegant borders"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Elegant double border frame
        outer_border = 12
        inner_border = 20
        
        # Outer border
        draw.rectangle([outer_border, outer_border, 
                       self.card_width - outer_border, self.card_height - outer_border], 
                      outline=colors['light'], width=1)
        
        # Inner border with professional thickness
        draw.rectangle([inner_border, inner_border, 
                       self.card_width - inner_border, self.card_height - inner_border], 
                      outline=colors['primary'], width=3)
        
        # Content positioning
        content_margin = inner_border + 25
        
        # Name with traditional elegance
        name_font = self.get_font_path('inter', 42, bold=True)
        name_y = 65
        draw.text((content_margin, name_y), card_data.get('name', ''), 
                 fill=colors['primary'], font=name_font)
        
        # Classic ornamental divider
        divider_y = name_y + 60
        divider_start = content_margin
        divider_end = self.card_width - content_margin
        
        # Main divider line
        draw.rectangle([divider_start, divider_y, divider_end, divider_y + 2], 
                      fill=colors['primary'])
        
        # Ornamental dots
        dot_spacing = 15
        for i in range(3):
            dot_x = divider_start + (i * dot_spacing)
            draw.ellipse([dot_x - 2, divider_y - 4, dot_x + 2, divider_y + 6], 
                        fill=colors['accent'])
        
        # Professional information hierarchy
        title_font = self.get_font_path('inter', 24, bold=False)
        company_font = self.get_font_path('inter', 22, bold=True)
        
        info_y = divider_y + 30
        draw.text((content_margin, info_y), card_data.get('job_title', ''), 
                 fill=colors['text'], font=title_font)
        
        draw.text((content_margin, info_y + 35), card_data.get('company', ''), 
                 fill=colors['accent'], font=company_font)
        
        # Contact details with classic formatting
        contact_font = self.get_font_path('inter', 18)
        contact_y = info_y + 85
        
        contact_items = [
            card_data.get('email', ''),
            card_data.get('phone', ''),
            card_data.get('website', '')
        ]
        
        for item in contact_items:
            if item:
                draw.text((content_margin, contact_y), item, 
                         fill=colors['text'], font=contact_font)
                contact_y += 28
        
        return img

    def creative_template(self, card_data, colors):
        """Creative template with geometric shapes"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Background shapes - larger and more impactful
        draw.ellipse([self.card_width-250, -60, self.card_width+60, 250], fill=colors['secondary'])
        draw.rectangle([0, self.card_height-100, 350, self.card_height], fill=colors['primary'])
        
        # Name - larger and better positioned
        name_font = self.get_font_path('inter', 52, bold=True)
        draw.text((self.margin, 80), card_data.get('name', ''), fill=colors['primary'], font=name_font)
        
        # Job title - larger
        title_font = self.get_font_path('inter', 28)
        draw.text((self.margin, 150), card_data.get('job_title', ''), fill=colors['text'], font=title_font)
        
        # Company - better size
        company_font = self.get_font_path('inter', 24)
        draw.text((self.margin, 190), card_data.get('company', ''), fill=colors['accent'], font=company_font)
        
        # Contact info - larger and better spaced
        contact_font = self.get_font_path('inter', 20)
        y_pos = 250
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill=colors['text'], font=contact_font)
                y_pos += 32
        
        return img

    def elegant_template(self, card_data, colors):
        """Luxury elegant template with sophisticated design elements"""
        img = Image.new('RGB', (self.card_width, self.card_height), colors['secondary'])
        draw = ImageDraw.Draw(img)
        
        # Luxury frame with multiple borders
        frame_outer = 20
        frame_middle = 28
        frame_inner = 35
        
        # Triple frame effect
        draw.rectangle([frame_outer, frame_outer, 
                       self.card_width - frame_outer, self.card_height - frame_outer], 
                      outline=colors['light'], width=1)
        
        draw.rectangle([frame_middle, frame_middle, 
                       self.card_width - frame_middle, self.card_height - frame_middle], 
                      outline=colors['accent'], width=1)
        
        draw.rectangle([frame_inner, frame_inner, 
                       self.card_width - frame_inner, self.card_height - frame_inner], 
                      outline=colors['primary'], width=2)
        
        # Elegant corner ornaments
        corner_size = 15
        corners = [(frame_inner + 5, frame_inner + 5), 
                  (self.card_width - frame_inner - corner_size - 5, frame_inner + 5),
                  (frame_inner + 5, self.card_height - frame_inner - corner_size - 5),
                  (self.card_width - frame_inner - corner_size - 5, 
                   self.card_height - frame_inner - corner_size - 5)]
        
        for x, y in corners:
            draw.ellipse([x, y, x + corner_size, y + corner_size], 
                        fill=colors['accent'])
            draw.ellipse([x + 3, y + 3, x + corner_size - 3, y + corner_size - 3], 
                        fill=colors['secondary'])
        
        # Content area
        content_x = frame_inner + 25
        
        # Elegant name styling
        name_font = self.get_font_path('inter', 38, bold=True)
        name_y = 75
        draw.text((content_x, name_y), card_data.get('name', ''), 
                 fill=colors['primary'], font=name_font)
        
        # Sophisticated decorative element
        decoration_y = name_y + 55
        decoration_width = 120
        
        # Central diamond shape
        diamond_center = content_x + decoration_width // 2
        diamond_points = [
            (diamond_center - 8, decoration_y),
            (diamond_center, decoration_y - 6),
            (diamond_center + 8, decoration_y),
            (diamond_center, decoration_y + 6)
        ]
        draw.polygon(diamond_points, fill=colors['accent'])
        
        # Flanking lines
        draw.rectangle([content_x, decoration_y - 1, diamond_center - 15, decoration_y + 1], 
                      fill=colors['accent'])
        draw.rectangle([diamond_center + 15, decoration_y - 1, 
                       content_x + decoration_width, decoration_y + 1], 
                      fill=colors['accent'])
        
        # Professional information
        title_font = self.get_font_path('inter', 22)
        company_font = self.get_font_path('inter', 20, bold=True)
        
        info_y = decoration_y + 25
        draw.text((content_x, info_y), card_data.get('job_title', ''), 
                 fill=colors['text'], font=title_font)
        
        draw.text((content_x, info_y + 32), card_data.get('company', ''), 
                 fill=colors['accent'], font=company_font)
        
        # Contact information with elegant spacing
        contact_font = self.get_font_path('inter', 17)
        contact_y = info_y + 75
        
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((content_x, contact_y), card_data[field], 
                         fill=colors['text'], font=contact_font)
                contact_y += 28
        
        return img

    def tech_template(self, card_data, colors):
        """Cutting-edge technology template with digital aesthetics"""
        # Dark base for high-tech feel
        base_color = '#0a0a0a'
        img = Image.new('RGB', (self.card_width, self.card_height), base_color)
        draw = ImageDraw.Draw(img)
        
        # Sophisticated grid pattern
        grid_spacing = 30
        grid_color = '#1a1a1a'
        
        # Subtle grid lines
        for i in range(0, self.card_width, grid_spacing):
            draw.line([i, 0, i, self.card_height], fill=grid_color, width=1)
        for i in range(0, self.card_height, grid_spacing):
            draw.line([0, i, self.card_width, i], fill=grid_color, width=1)
        
        # High-tech accent panel with angle
        panel_width = 320
        angle_offset = 40
        
        # Main panel
        panel_points = [
            (0, 0),
            (panel_width, 0),
            (panel_width - angle_offset, self.card_height),
            (0, self.card_height)
        ]
        draw.polygon(panel_points, fill=colors['primary'])
        
        # Circuit-inspired accent lines
        circuit_color = colors['accent']
        
        # Horizontal circuit lines
        for y in [120, 180, 240]:
            draw.rectangle([20, y, panel_width - 60, y + 2], fill=circuit_color)
            
            # Circuit nodes
            node_size = 4
            for x in [30, 80, 130, 180]:
                if x < panel_width - 60:
                    draw.ellipse([x - node_size, y - node_size, 
                                 x + node_size, y + node_size], fill=circuit_color)
        
        # Name with tech styling
        name_font = self.get_font_path('inter', 40, bold=True)
        name_y = 45
        name_text = card_data.get('name', '').upper()
        
        # Glowing effect simulation
        glow_offset = 1
        draw.text((self.safe_margin + glow_offset, name_y + glow_offset), 
                 name_text, fill=colors['accent'], font=name_font)
        draw.text((self.safe_margin, name_y), name_text, 
                 fill='white', font=name_font)
        
        # Digital-style information display
        title_font = self.get_font_path('inter', 22)
        company_font = self.get_font_path('inter', 20)
        
        info_y = 140
        
        # Job title with bracket styling
        title_text = f"[ {card_data.get('job_title', '')} ]"
        draw.text((self.safe_margin, info_y), title_text, 
                 fill=colors['light'], font=title_font)
        
        # Company with tech formatting
        company_text = f"> {card_data.get('company', '')}"
        draw.text((self.safe_margin, info_y + 35), company_text, 
                 fill='white', font=company_font)
        
        # Contact data in terminal style
        contact_font = self.get_font_path('inter', 18)
        contact_y = 250
        
        contact_prefixes = ['@', '#', '$']
        contact_fields = [card_data.get('email', ''), 
                         card_data.get('phone', ''), 
                         card_data.get('website', '')]
        
        for i, (prefix, value) in enumerate(zip(contact_prefixes, contact_fields)):
            if value:
                display_text = f"{prefix} {value}"
                draw.text((self.safe_margin, contact_y), display_text, 
                         fill=colors['light'], font=contact_font)
                contact_y += 28
        
        return img

    def corporate_template(self, card_data, colors):
        """Corporate professional template"""
        return self.classic_template(card_data, colors)  # Similar to classic

    def artistic_template(self, card_data, colors):
        """Artistic template with creative elements"""
        return self.creative_template(card_data, colors)  # Similar to creative

    def minimal_template(self, card_data, colors):
        """Ultra-minimal professional template with perfect balance"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Minimal but sophisticated layout
        content_margin = 60
        
        # Name with perfect minimal typography
        name_font = self.get_font_path('inter', 46, bold=True)
        name_y = 80
        draw.text((content_margin, name_y), card_data.get('name', ''), 
                 fill=colors['text'], font=name_font)
        
        # Geometric accent element
        accent_y = name_y + 65
        accent_length = 150
        accent_thickness = 3
        
        # Main accent line
        draw.rectangle([content_margin, accent_y, 
                       content_margin + accent_length, accent_y + accent_thickness], 
                      fill=colors['primary'])
        
        # Minimal geometric shape
        square_size = 8
        square_x = content_margin + accent_length + 15
        draw.rectangle([square_x, accent_y - 2, 
                       square_x + square_size, accent_y + square_size + 1], 
                      fill=colors['accent'])
        
        # Professional hierarchy with perfect spacing
        title_font = self.get_font_path('inter', 22)
        company_font = self.get_font_path('inter', 20)
        
        info_y = accent_y + 35
        draw.text((content_margin, info_y), card_data.get('job_title', ''), 
                 fill=colors['accent'], font=title_font)
        
        draw.text((content_margin, info_y + 35), card_data.get('company', ''), 
                 fill=colors['text'], font=company_font)
        
        # Minimal contact layout
        contact_font = self.get_font_path('inter', 18)
        contact_y = info_y + 85
        
        # Create clean, spaced contact list
        contacts = [card_data.get('email', ''), card_data.get('phone', ''), 
                   card_data.get('website', '')]
        
        for contact in contacts:
            if contact:
                draw.text((content_margin, contact_y), contact, 
                         fill=colors['text'], font=contact_font)
                contact_y += 30
        
        return img

    def bold_template(self, card_data, colors):
        """Bold impactful template"""
        img = Image.new('RGB', (self.card_width, self.card_height), colors['primary'])
        draw = ImageDraw.Draw(img)
        
        # Bold design elements - taller header
        draw.rectangle([0, 0, self.card_width, 170], fill=colors['text'])
        
        # Name in bold - larger
        name_font = self.get_font_path('inter', 60, bold=True)
        draw.text((self.margin, 50), card_data.get('name', ''), fill='white', font=name_font)
        
        # Job title - larger
        title_font = self.get_font_path('inter', 32, bold=True)
        draw.text((self.margin, 200), card_data.get('job_title', ''), fill='white', font=title_font)
        
        # Company - better size
        company_font = self.get_font_path('inter', 26)
        draw.text((self.margin, 250), card_data.get('company', ''), fill=colors['secondary'], font=company_font)
        
        # Contact info - larger and bold
        contact_font = self.get_font_path('inter', 22, bold=True)
        y_pos = 310
        for field in ['email', 'phone', 'website']:
            if card_data.get(field):
                draw.text((self.margin, y_pos), card_data[field], fill='white', font=contact_font)
                y_pos += 35
        
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
        """Premium executive template with authoritative design"""
        img = Image.new('RGB', (self.card_width, self.card_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Executive power strip design
        header_height = 130
        
        # Main header block
        draw.rectangle([0, 0, self.card_width, header_height], fill=colors['primary'])
        
        # Accent stripe
        stripe_height = 8
        draw.rectangle([0, header_height, self.card_width, header_height + stripe_height], 
                      fill=colors['accent'])
        
        # Subtle gradient effect simulation
        gradient_height = 25
        for i in range(gradient_height):
            alpha = int(255 * (1 - i / gradient_height) * 0.1)
            gradient_color = colors['dark'] + f'{alpha:02x}'
            try:
                # Create gradient overlay
                gradient_line = Image.new('RGBA', (self.card_width, 1), gradient_color)
                img.paste(gradient_line, (0, i), gradient_line)
            except:
                pass
        
        # Executive name positioning
        name_font = self.get_font_path('inter', 44, bold=True)
        name_x = self.safe_margin
        name_y = 35
        
        # Drop shadow effect for name
        shadow_offset = 2
        draw.text((name_x + shadow_offset, name_y + shadow_offset), 
                 card_data.get('name', ''), fill=colors['dark'], font=name_font)
        draw.text((name_x, name_y), card_data.get('name', ''), 
                 fill='white', font=name_font)
        
        # Professional credentials area
        content_y = header_height + stripe_height + 25
        
        # Job title with authority
        title_font = self.get_font_path('inter', 26, bold=True)
        draw.text((name_x, content_y), card_data.get('job_title', ''), 
                 fill=colors['primary'], font=title_font)
        
        # Company with prestige styling
        company_font = self.get_font_path('inter', 22)
        company_y = content_y + 40
        draw.text((name_x, company_y), card_data.get('company', ''), 
                 fill=colors['text'], font=company_font)
        
        # Executive divider with sophisticated design
        divider_y = company_y + 50
        divider_length = 200
        
        # Main divider
        draw.rectangle([name_x, divider_y, name_x + divider_length, divider_y + 2], 
                      fill=colors['accent'])
        
        # End caps
        cap_size = 6
        draw.ellipse([name_x - cap_size//2, divider_y - cap_size//2, 
                     name_x + cap_size//2, divider_y + cap_size//2], 
                    fill=colors['primary'])
        draw.ellipse([name_x + divider_length - cap_size//2, divider_y - cap_size//2, 
                     name_x + divider_length + cap_size//2, divider_y + cap_size//2], 
                    fill=colors['primary'])
        
        # Executive contact information
        contact_font = self.get_font_path('inter', 19)
        contact_y = divider_y + 25
        
        contact_fields = [
            ('email', card_data.get('email', '')),
            ('phone', card_data.get('phone', '')),
            ('website', card_data.get('website', ''))
        ]
        
        for label, value in contact_fields:
            if value:
                draw.text((name_x, contact_y), value, 
                         fill=colors['text'], font=contact_font)
                contact_y += 30
        
        return img

    def generate_card(self, card_data):
        """Generate business card image"""
        template_name = card_data.get('template', 'modern')
        color_scheme = card_data.get('color_scheme', 'blue')
        
        colors = self.color_schemes.get(color_scheme, self.color_schemes['corporate_blue'])
        template_func = self.templates.get(template_name, self.modern_template)
        
        # Generate base card
        card_img = template_func(card_data, colors)
        
        # Add logo if provided
        if card_data.get('logo_path') and os.path.exists(card_data['logo_path']):
            try:
                logo = Image.open(card_data['logo_path'])
                
                # Make logo larger and more prominent
                max_logo_size = (150, 150)
                logo.thumbnail(max_logo_size, Image.Resampling.LANCZOS)
                
                # Better positioning - more visible in top-right corner
                logo_margin = 30  # Reduce margin for better visibility
                logo_x = self.card_width - logo.width - logo_margin
                logo_y = logo_margin
                
                # Add subtle white background for better contrast
                logo_bg = Image.new('RGBA', (logo.width + 10, logo.height + 10), (255, 255, 255, 200))
                logo_bg_x = logo_x - 5
                logo_bg_y = logo_y - 5
                
                # Paste background first, then logo
                if logo_bg.mode == 'RGBA':
                    card_img.paste(logo_bg, (logo_bg_x, logo_bg_y), logo_bg)
                else:
                    card_img.paste(logo_bg, (logo_bg_x, logo_bg_y))
                
                # Paste the logo
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
