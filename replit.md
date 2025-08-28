# CardGen - Business Card Generator

## Overview

CardGen is a mobile-first Progressive Web App (PWA) that allows users to create, customize, and export professional business cards. The application features 13+ professional templates, 15+ color schemes, QR code integration, and multiple export formats including PNG, PDF, and batch processing capabilities. Built with a focus on mobile usability and native app-like experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Mobile-First PWA Design**: Progressive Web App with service worker caching, app manifest, and mobile status bar simulation
- **Responsive UI Framework**: Bootstrap 5 with custom mobile-optimized CSS overrides and touch-friendly interactions
- **Component Structure**: Modular JavaScript classes for template management, card preview, and app functionality
- **Template System**: Jinja2-based templating with base template inheritance and component reusability
- **Asset Management**: Static file organization with CSS, JS, and manifest files for PWA functionality

### Backend Architecture
- **Web Framework**: Flask application with modular route separation and session-based state management
- **Image Processing Pipeline**: PIL/Pillow for card generation, template rendering, and logo handling
- **Document Generation**: ReportLab for PDF creation with both standard and print-ready CMYK output
- **File Upload System**: Secure file handling with validation, size limits (16MB), and sanitization using Werkzeug
- **Session Management**: Flask sessions for persistent user data across form steps

### Data Storage
- **Session-Based Storage**: User card data stored in Flask sessions for temporary persistence
- **File System Storage**: Uploaded logos and generated previews stored in organized directory structure
- **No Database Dependency**: Stateless design with form-based data flow and file-based operations

### Card Generation System
- **Template Engine**: 13+ professional card templates with customizable layouts and styling
- **Color Scheme System**: 15+ predefined color palettes with primary, secondary, accent, and text colors
- **QR Code Integration**: vCard QR code generation for contact sharing functionality
- **Multi-Format Export**: PNG (high-res), PDF (standard), PDF (print-ready), and HTML (interactive) outputs
- **Batch Processing**: CSV upload support for generating multiple cards as ZIP archives

## External Dependencies

### Core Libraries
- **Flask**: Web framework for routing, templating, and request handling
- **PIL (Pillow)**: Image processing for card generation and logo manipulation
- **ReportLab**: PDF document generation with vector graphics support
- **qrcode**: QR code generation for vCard contact information

### Frontend Dependencies
- **Bootstrap 5**: CSS framework delivered via CDN for responsive design
- **Font Awesome 6**: Icon library via CDN for consistent iconography
- **Inter Font**: Typography via Google Fonts API for modern, readable interface

### PWA Infrastructure
- **Service Worker**: Custom caching strategy for offline functionality
- **Web App Manifest**: PWA configuration for installable app experience
- **Touch and Haptic APIs**: Native mobile interaction support

### File Processing
- **Werkzeug**: Secure filename handling and file upload utilities
- **CSV Module**: Built-in Python library for batch processing functionality
- **ZipFile**: Built-in Python library for archive creation and export