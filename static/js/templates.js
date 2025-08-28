// Template selection and customization functionality
class TemplateManager {
    constructor() {
        this.selectedTemplate = 'modern';
        this.selectedColorScheme = 'blue';
        this.selectedFont = 'inter';
        this.init();
    }

    init() {
        this.setupTemplateSelection();
        this.setupColorSelection();
        this.setupFontSelection();
        this.setupPreviewUpdates();
        this.loadSavedSelections();
    }

    setupTemplateSelection() {
        const templateOptions = document.querySelectorAll('input[name="template"]');
        
        templateOptions.forEach(option => {
            option.addEventListener('change', (e) => {
                this.selectedTemplate = e.target.value;
                this.updateTemplateSelection(e.target);
                this.updateLivePreview();
                this.saveSelections();
                
                // Haptic feedback
                if (window.app) {
                    window.app.triggerHaptic('light');
                }
            });
        });

        // Add hover effects for template previews
        const templateLabels = document.querySelectorAll('.template-option');
        templateLabels.forEach(label => {
            label.addEventListener('mouseenter', () => {
                this.showTemplateTooltip(label);
            });
            
            label.addEventListener('mouseleave', () => {
                this.hideTemplateTooltip();
            });
        });
    }

    setupColorSelection() {
        const colorOptions = document.querySelectorAll('input[name="color_scheme"]');
        
        colorOptions.forEach(option => {
            option.addEventListener('change', (e) => {
                this.selectedColorScheme = e.target.value;
                this.updateColorSelection(e.target);
                this.updateLivePreview();
                this.saveSelections();
                
                // Haptic feedback
                if (window.app) {
                    window.app.triggerHaptic('light');
                }
            });
        });

        // Add color scheme preview on hover
        const colorLabels = document.querySelectorAll('.color-option');
        colorLabels.forEach(label => {
            label.addEventListener('mouseenter', () => {
                this.previewColorScheme(label);
            });
            
            label.addEventListener('mouseleave', () => {
                this.resetColorPreview();
            });
        });
    }

    setupFontSelection() {
        const fontSelect = document.getElementById('font_family');
        if (fontSelect) {
            fontSelect.addEventListener('change', (e) => {
                this.selectedFont = e.target.value;
                this.updateFontPreview();
                this.updateLivePreview();
                this.saveSelections();
            });
        }

        const textAlignSelect = document.getElementById('text_align');
        if (textAlignSelect) {
            textAlignSelect.addEventListener('change', () => {
                this.updateLivePreview();
                this.saveSelections();
            });
        }
    }

    setupPreviewUpdates() {
        // Watch for form field changes to update preview
        const formFields = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], input[type="url"], textarea, select');
        
        formFields.forEach(field => {
            field.addEventListener('input', () => {
                this.debouncePreviewUpdate();
            });
            
            field.addEventListener('change', () => {
                this.updateLivePreview();
            });
        });

        // Watch for checkbox changes
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateLivePreview();
            });
        });
    }

    updateTemplateSelection(selectedInput) {
        // Remove selected class from all options
        document.querySelectorAll('.template-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selected class to chosen option
        selectedInput.closest('.template-option').classList.add('selected');
        
        // Update template preview
        this.updateTemplatePreview(selectedInput.value);
        
        // Show template change animation
        this.showTemplateChangeAnimation(selectedInput.value);
    }

    updateColorSelection(selectedInput) {
        // Remove selected class from all options
        document.querySelectorAll('.color-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selected class to chosen option
        selectedInput.closest('.color-option').classList.add('selected');
        
        // Update color preview
        this.updateColorPreview(selectedInput.value);
    }

    updateTemplatePreview(templateName) {
        const previewElements = document.querySelectorAll('.template-preview');
        previewElements.forEach(preview => {
            if (preview.classList.contains(templateName)) {
                preview.classList.add('active-preview');
            } else {
                preview.classList.remove('active-preview');
            }
        });
    }

    updateColorPreview(colorScheme) {
        // Update any color preview elements
        const colorPreviewElements = document.querySelectorAll('.color-preview');
        colorPreviewElements.forEach(element => {
            element.className = `color-preview ${colorScheme}`;
        });
    }

    updateFontPreview() {
        // Update font preview in the form
        const fontPreviewElements = document.querySelectorAll('.font-preview');
        fontPreviewElements.forEach(element => {
            element.style.fontFamily = this.getFontFamily(this.selectedFont);
        });
    }

    getFontFamily(fontKey) {
        const fontMap = {
            'inter': '"Inter", sans-serif',
            'roboto': '"Roboto", sans-serif',
            'open_sans': '"Open Sans", sans-serif',
            'lato': '"Lato", sans-serif',
            'montserrat': '"Montserrat", sans-serif',
            'poppins': '"Poppins", sans-serif',
            'nunito': '"Nunito", sans-serif',
            'source_sans': '"Source Sans Pro", sans-serif',
            'ubuntu': '"Ubuntu", sans-serif',
            'raleway': '"Raleway", sans-serif',
            'oswald': '"Oswald", sans-serif',
            'merriweather': '"Merriweather", serif'
        };
        
        return fontMap[fontKey] || fontMap.inter;
    }

    showTemplateTooltip(label) {
        const templateName = label.querySelector('input').value;
        const templateDisplayName = label.querySelector('.template-name').textContent;
        
        let tooltip = document.getElementById('template-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'template-tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: var(--text-color);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                z-index: 1000;
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
                white-space: nowrap;
            `;
            document.body.appendChild(tooltip);
        }
        
        const rect = label.getBoundingClientRect();
        tooltip.textContent = `${templateDisplayName} Template`;
        tooltip.style.left = `${rect.left + rect.width/2 - tooltip.offsetWidth/2}px`;
        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
        tooltip.style.opacity = '1';
    }

    hideTemplateTooltip() {
        const tooltip = document.getElementById('template-tooltip');
        if (tooltip) {
            tooltip.style.opacity = '0';
        }
    }

    previewColorScheme(label) {
        const colorValue = label.querySelector('input').value;
        // Could implement live color preview here
    }

    resetColorPreview() {
        // Reset any temporary color previews
    }

    showTemplateChangeAnimation(templateName) {
        // Create a brief animation to show template change
        const indicator = document.createElement('div');
        indicator.className = 'template-change-indicator';
        indicator.textContent = `Switched to ${templateName.charAt(0).toUpperCase() + templateName.slice(1)} template`;
        indicator.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--primary-color);
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            font-size: 14px;
            z-index: 1070;
            opacity: 0;
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(indicator);
        
        setTimeout(() => {
            indicator.style.opacity = '1';
            indicator.style.transform = 'translate(-50%, -50%) scale(1.05)';
        }, 10);
        
        setTimeout(() => {
            indicator.style.opacity = '0';
            indicator.style.transform = 'translate(-50%, -50%) scale(0.95)';
            setTimeout(() => {
                indicator.remove();
            }, 300);
        }, 1500);
    }

    updateLivePreview() {
        // If on preview page, could update preview in real-time
        if (window.location.pathname.includes('preview')) {
            this.debouncePreviewUpdate();
        }
    }

    debouncePreviewUpdate() {
        clearTimeout(this.previewUpdateTimeout);
        this.previewUpdateTimeout = setTimeout(() => {
            this.performPreviewUpdate();
        }, 500);
    }

    performPreviewUpdate() {
        // This would trigger a preview update
        // For now, just show that preview would update
        const previewIndicator = document.querySelector('.preview-update-indicator');
        if (previewIndicator) {
            previewIndicator.style.opacity = '1';
            setTimeout(() => {
                previewIndicator.style.opacity = '0';
            }, 1000);
        }
    }

    saveSelections() {
        const selections = {
            template: this.selectedTemplate,
            colorScheme: this.selectedColorScheme,
            font: this.selectedFont,
            timestamp: Date.now()
        };
        
        localStorage.setItem('templateSelections', JSON.stringify(selections));
    }

    loadSavedSelections() {
        const saved = localStorage.getItem('templateSelections');
        if (saved) {
            try {
                const selections = JSON.parse(saved);
                
                // Only load if saved recently (within 24 hours)
                if (Date.now() - selections.timestamp < 24 * 60 * 60 * 1000) {
                    this.selectedTemplate = selections.template || 'modern';
                    this.selectedColorScheme = selections.colorScheme || 'blue';
                    this.selectedFont = selections.font || 'inter';
                    
                    this.applyLoadedSelections();
                }
            } catch (e) {
                console.log('Could not load saved template selections');
            }
        }
    }

    applyLoadedSelections() {
        // Apply template selection
        const templateInput = document.querySelector(`input[name="template"][value="${this.selectedTemplate}"]`);
        if (templateInput) {
            templateInput.checked = true;
            this.updateTemplateSelection(templateInput);
        }
        
        // Apply color selection
        const colorInput = document.querySelector(`input[name="color_scheme"][value="${this.selectedColorScheme}"]`);
        if (colorInput) {
            colorInput.checked = true;
            this.updateColorSelection(colorInput);
        }
        
        // Apply font selection
        const fontSelect = document.getElementById('font_family');
        if (fontSelect) {
            fontSelect.value = this.selectedFont;
            this.updateFontPreview();
        }
    }

    // Template preview animations
    animateTemplatePreview(templateElement) {
        templateElement.style.transform = 'scale(1.05)';
        templateElement.style.transition = 'transform 0.2s ease';
        
        setTimeout(() => {
            templateElement.style.transform = 'scale(1)';
        }, 200);
    }

    // Accessibility improvements
    setupKeyboardNavigation() {
        const templateOptions = document.querySelectorAll('.template-option');
        const colorOptions = document.querySelectorAll('.color-option');
        
        [...templateOptions, ...colorOptions].forEach((option, index) => {
            option.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    option.querySelector('input').click();
                }
                
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextOption = option.nextElementSibling || option.parentElement.firstElementChild;
                    nextOption.focus();
                }
                
                if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevOption = option.previousElementSibling || option.parentElement.lastElementChild;
                    prevOption.focus();
                }
            });
        });
    }

    // Template recommendations
    getRecommendedTemplates(userInput) {
        const recommendations = {
            'tech': ['tech', 'modern', 'minimal'],
            'creative': ['creative', 'artistic', 'bold'],
            'business': ['corporate', 'executive', 'classic'],
            'design': ['elegant', 'gradient', 'geometric']
        };
        
        // Simple keyword matching
        for (const [category, templates] of Object.entries(recommendations)) {
            if (userInput.toLowerCase().includes(category)) {
                return templates;
            }
        }
        
        return ['modern', 'classic', 'elegant']; // Default recommendations
    }

    showRecommendations() {
        const jobTitle = document.getElementById('job_title')?.value || '';
        const company = document.getElementById('company')?.value || '';
        const combined = `${jobTitle} ${company}`.toLowerCase();
        
        if (combined.trim()) {
            const recommended = this.getRecommendedTemplates(combined);
            this.highlightRecommendedTemplates(recommended);
        }
    }

    highlightRecommendedTemplates(templates) {
        // Remove existing recommendations
        document.querySelectorAll('.template-option').forEach(option => {
            option.classList.remove('recommended');
        });
        
        // Add recommendation highlight
        templates.forEach(templateName => {
            const option = document.querySelector(`input[value="${templateName}"]`)?.closest('.template-option');
            if (option) {
                option.classList.add('recommended');
            }
        });
        
        // Show recommendation notice
        this.showRecommendationNotice(templates);
    }

    showRecommendationNotice(templates) {
        let notice = document.getElementById('recommendation-notice');
        if (!notice) {
            notice = document.createElement('div');
            notice.id = 'recommendation-notice';
            notice.className = 'alert alert-info recommendation-notice';
            notice.style.cssText = `
                margin-bottom: 1rem;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            
            const templateGrid = document.querySelector('.template-grid');
            if (templateGrid) {
                templateGrid.parentNode.insertBefore(notice, templateGrid);
            }
        }
        
        notice.innerHTML = `
            <i class="fas fa-lightbulb"></i>
            <strong>Recommended templates</strong> based on your information are highlighted
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        notice.style.opacity = '1';
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (notice.parentNode) {
                notice.style.opacity = '0';
                setTimeout(() => {
                    notice.remove();
                }, 300);
            }
        }, 10000);
    }
}

// CSS for template recommendations
const recommendationStyles = document.createElement('style');
recommendationStyles.textContent = `
    .template-option.recommended {
        border-color: #f59e0b !important;
        background: linear-gradient(135deg, #fef3c7, #ffffff) !important;
        position: relative;
    }
    
    .template-option.recommended::before {
        content: "★";
        position: absolute;
        top: -5px;
        right: -5px;
        background: #f59e0b;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        z-index: 1;
    }
    
    .template-preview.active-preview {
        box-shadow: 0 0 0 3px var(--primary-color);
        transform: scale(1.05);
    }
`;
document.head.appendChild(recommendationStyles);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.template-grid')) {
        window.templateManager = new TemplateManager();
        
        // Set up job title/company change listeners for recommendations
        ['job_title', 'company'].forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', () => {
                    setTimeout(() => {
                        window.templateManager.showRecommendations();
                    }, 1000);
                });
            }
        });
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TemplateManager;
}
