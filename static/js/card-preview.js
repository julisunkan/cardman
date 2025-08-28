// Card Preview functionality
class CardPreview {
    constructor() {
        this.init();
        this.setupEventListeners();
    }

    init() {
        this.previewImage = document.getElementById('card-preview');
        this.isZoomed = false;
        this.zoomLevel = 1;
        this.maxZoom = 3;
        this.minZoom = 1;
        
        if (this.previewImage) {
            this.setupZoom();
            this.setupPanAndZoom();
        }
    }

    setupEventListeners() {
        // Export button loading states
        document.querySelectorAll('.export-option').forEach(option => {
            option.addEventListener('click', (e) => {
                this.handleExportClick(e, option);
            });
        });

        // Preview refresh
        const refreshBtn = document.querySelector('[data-action="refresh-preview"]');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshPreview();
            });
        }

        // Share functionality
        const shareBtn = document.querySelector('[data-action="share"]');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => {
                this.shareCard();
            });
        }

        // Full screen toggle
        const fullscreenBtn = document.querySelector('[data-action="fullscreen"]');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                this.toggleFullscreen();
            });
        }
    }

    setupZoom() {
        if (!this.previewImage) return;

        // Click to zoom
        this.previewImage.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleZoom();
        });

        // Double tap to zoom
        let lastTap = 0;
        this.previewImage.addEventListener('touchend', (e) => {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;
            
            if (tapLength < 500 && tapLength > 0) {
                e.preventDefault();
                this.toggleZoom();
            }
            lastTap = currentTime;
        });
    }

    setupPanAndZoom() {
        if (!this.previewImage) return;

        let isPanning = false;
        let startX, startY;
        let translateX = 0, translateY = 0;

        // Touch events for pan
        this.previewImage.addEventListener('touchstart', (e) => {
            if (this.isZoomed && e.touches.length === 1) {
                isPanning = true;
                startX = e.touches[0].clientX - translateX;
                startY = e.touches[0].clientY - translateY;
                this.previewImage.style.cursor = 'grabbing';
            }
        });

        this.previewImage.addEventListener('touchmove', (e) => {
            if (!isPanning || !this.isZoomed) return;
            
            e.preventDefault();
            translateX = e.touches[0].clientX - startX;
            translateY = e.touches[0].clientY - startY;
            
            this.updateTransform(translateX, translateY);
        });

        this.previewImage.addEventListener('touchend', () => {
            isPanning = false;
            this.previewImage.style.cursor = this.isZoomed ? 'grab' : 'zoom-in';
        });

        // Pinch to zoom
        let initialDistance = 0;
        let initialZoom = 1;

        this.previewImage.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                initialDistance = this.getDistance(e.touches[0], e.touches[1]);
                initialZoom = this.zoomLevel;
            }
        });

        this.previewImage.addEventListener('touchmove', (e) => {
            if (e.touches.length === 2) {
                e.preventDefault();
                const currentDistance = this.getDistance(e.touches[0], e.touches[1]);
                const scale = currentDistance / initialDistance;
                this.zoomLevel = Math.min(Math.max(initialZoom * scale, this.minZoom), this.maxZoom);
                
                this.updateTransform(translateX, translateY, this.zoomLevel);
                
                if (this.zoomLevel > 1) {
                    this.isZoomed = true;
                    this.previewImage.style.cursor = 'grab';
                } else {
                    this.isZoomed = false;
                    this.previewImage.style.cursor = 'zoom-in';
                    translateX = 0;
                    translateY = 0;
                }
            }
        });
    }

    getDistance(touch1, touch2) {
        const dx = touch2.clientX - touch1.clientX;
        const dy = touch2.clientY - touch1.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    toggleZoom() {
        if (this.isZoomed) {
            this.zoomOut();
        } else {
            this.zoomIn();
        }
    }

    zoomIn() {
        this.isZoomed = true;
        this.zoomLevel = 2;
        this.previewImage.style.cursor = 'grab';
        this.updateTransform(0, 0, this.zoomLevel);
        
        // Add zoom indicator
        this.showZoomIndicator('Tap to zoom out');
    }

    zoomOut() {
        this.isZoomed = false;
        this.zoomLevel = 1;
        this.previewImage.style.cursor = 'zoom-in';
        this.updateTransform(0, 0, this.zoomLevel);
        
        // Add zoom indicator
        this.showZoomIndicator('Tap to zoom in');
    }

    updateTransform(x = 0, y = 0, scale = this.zoomLevel) {
        this.previewImage.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
        this.previewImage.style.transformOrigin = 'center';
        this.previewImage.style.transition = scale === 1 ? 'transform 0.3s ease' : 'none';
    }

    showZoomIndicator(text) {
        let indicator = document.getElementById('zoom-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'zoom-indicator';
            indicator.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 14px;
                z-index: 1070;
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
            `;
            document.body.appendChild(indicator);
        }
        
        indicator.textContent = text;
        indicator.style.opacity = '1';
        
        setTimeout(() => {
            indicator.style.opacity = '0';
        }, 1500);
    }

    handleExportClick(event, option) {
        const originalContent = option.innerHTML;
        const exportType = option.href.split('/').pop();
        
        // Show loading state
        option.innerHTML = option.innerHTML.replace(
            /fas fa-[\w-]+/,
            'fas fa-spinner fa-spin'
        );
        option.style.pointerEvents = 'none';
        
        // Show progress notification
        const notification = this.showExportProgress(exportType);
        
        // Simulate export process (actual export happens on server)
        setTimeout(() => {
            option.innerHTML = originalContent;
            option.style.pointerEvents = 'auto';
            
            // Update notification
            notification.className = notification.className.replace('alert-info', 'alert-success');
            notification.innerHTML = `
                <i class="fas fa-check"></i>
                ${exportType.toUpperCase()} export ready! Download should start automatically.
            `;
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
            
            // Trigger haptic feedback
            if (window.app) {
                window.app.triggerHaptic('medium');
            }
        }, 2000);
    }

    showExportProgress(type) {
        const notification = document.createElement('div');
        notification.className = 'alert alert-info export-progress';
        notification.innerHTML = `
            <i class="fas fa-cogs fa-spin"></i>
            Generating ${type.toUpperCase()} export...
        `;
        notification.style.cssText = `
            position: fixed;
            top: 110px;
            left: 20px;
            right: 20px;
            z-index: 1060;
            opacity: 0;
            transform: translateY(-20px);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 100);
        
        return notification;
    }

    refreshPreview() {
        if (!this.previewImage) return;
        
        const src = this.previewImage.src;
        const timestamp = new Date().getTime();
        const newSrc = src.includes('?') ? `${src}&t=${timestamp}` : `${src}?t=${timestamp}`;
        
        // Show loading state
        this.previewImage.style.opacity = '0.5';
        
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'preview-loading';
        loadingIndicator.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        loadingIndicator.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2rem;
            color: var(--primary-color);
            z-index: 10;
        `;
        
        this.previewImage.parentElement.style.position = 'relative';
        this.previewImage.parentElement.appendChild(loadingIndicator);
        
        // Reload image
        const img = new Image();
        img.onload = () => {
            this.previewImage.src = newSrc;
            this.previewImage.style.opacity = '1';
            loadingIndicator.remove();
            
            if (window.app) {
                window.app.showNotification('Preview updated!', 'success');
            }
        };
        
        img.onerror = () => {
            this.previewImage.style.opacity = '1';
            loadingIndicator.remove();
            
            if (window.app) {
                window.app.showNotification('Failed to update preview', 'error');
            }
        };
        
        img.src = newSrc;
    }

    shareCard() {
        if (navigator.share) {
            // Use native sharing if available
            navigator.share({
                title: 'My Business Card',
                text: 'Check out my business card!',
                url: window.location.href
            }).catch(console.error);
        } else {
            // Fallback to copy link
            window.CardApp.copyToClipboard(window.location.href);
        }
    }

    toggleFullscreen() {
        if (!this.previewImage) return;
        
        const fullscreenContainer = document.createElement('div');
        fullscreenContainer.className = 'fullscreen-preview';
        fullscreenContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        const fullscreenImage = this.previewImage.cloneNode();
        fullscreenImage.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        `;
        
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '<i class="fas fa-times"></i>';
        closeButton.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            font-size: 1.5rem;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        fullscreenContainer.appendChild(fullscreenImage);
        fullscreenContainer.appendChild(closeButton);
        document.body.appendChild(fullscreenContainer);
        
        // Animate in
        setTimeout(() => {
            fullscreenContainer.style.opacity = '1';
        }, 10);
        
        // Close handlers
        const closeFullscreen = () => {
            fullscreenContainer.style.opacity = '0';
            setTimeout(() => {
                fullscreenContainer.remove();
            }, 300);
        };
        
        closeButton.addEventListener('click', closeFullscreen);
        fullscreenContainer.addEventListener('click', (e) => {
            if (e.target === fullscreenContainer) {
                closeFullscreen();
            }
        });
        
        // Escape key
        const escapeHandler = (e) => {
            if (e.key === 'Escape') {
                closeFullscreen();
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);
    }

    // Compare current card with saved version
    compareWithSaved() {
        const savedData = localStorage.getItem('autoSave_form');
        if (savedData) {
            const { timestamp } = JSON.parse(savedData);
            const timeDiff = Date.now() - timestamp;
            
            if (timeDiff < 60000) { // Less than 1 minute
                this.showComparisonNotice();
            }
        }
    }

    showComparisonNotice() {
        const notice = document.createElement('div');
        notice.className = 'alert alert-info comparison-notice';
        notice.innerHTML = `
            <i class="fas fa-info-circle"></i>
            Your card data was recently modified. 
            <a href="#" onclick="location.reload()" class="alert-link">Refresh to see latest changes</a>
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        const header = document.querySelector('.page-header');
        if (header) {
            header.parentNode.insertBefore(notice, header.nextSibling);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('card-preview')) {
        window.cardPreview = new CardPreview();
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CardPreview;
}
