// App initialization and global functionality
class MobileCardApp {
    constructor() {
        this.init();
        this.registerServiceWorker();
        this.setupEventListeners();
        this.updateStatusBar();
        this.initializeTouch();
    }

    init() {
        console.log('CardGen App initialized');
        
        // Set up viewport for mobile
        if (!document.querySelector('meta[name="viewport"]')) {
            const viewport = document.createElement('meta');
            viewport.name = 'viewport';
            viewport.content = 'width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover';
            document.head.appendChild(viewport);
        }

        // Add touch class to body for CSS targeting
        document.body.classList.add('touch-device');
        
        // Initialize PWA features
        this.initPWA();
    }

    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/sw.js')
                    .then(registration => {
                        console.log('SW registered: ', registration);
                    })
                    .catch(registrationError => {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
    }

    setupEventListeners() {
        // Back button handling
        window.addEventListener('popstate', this.handleBackButton.bind(this));
        
        // Network status
        window.addEventListener('online', this.handleOnline.bind(this));
        window.addEventListener('offline', this.handleOffline.bind(this));
        
        // App lifecycle
        document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
        
        // Touch events for haptic feedback
        this.setupHapticFeedback();
        
        // Form auto-save
        this.setupAutoSave();
        
        // Pull to refresh
        this.setupPullToRefresh();
    }

    updateStatusBar() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const updateTime = () => {
                const now = new Date();
                timeElement.textContent = now.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit'
                });
            };
            
            updateTime();
            setInterval(updateTime, 1000);
        }
    }

    initializeTouch() {
        // Add touch ripple effect
        document.addEventListener('touchstart', (e) => {
            const target = e.target.closest('.touch-target, .btn, .nav-item, .template-option, .color-option, .export-option, .action-card, .feature-card');
            if (target && !target.classList.contains('no-ripple')) {
                this.createRipple(e, target);
            }
        });

        // Handle touch feedback
        document.addEventListener('touchstart', (e) => {
            const target = e.target.closest('.touch-feedback');
            if (target) {
                target.classList.add('touched');
            }
        });

        document.addEventListener('touchend', (e) => {
            const target = e.target.closest('.touch-feedback');
            if (target) {
                setTimeout(() => {
                    target.classList.remove('touched');
                }, 150);
            }
        });
    }

    createRipple(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.touches[0].clientX - rect.left - size / 2;
        const y = event.touches[0].clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    setupHapticFeedback() {
        // Simulate haptic feedback for supported actions
        const hapticElements = document.querySelectorAll('.btn-primary, .nav-item, .template-option.selected, .color-option.selected');
        
        hapticElements.forEach(element => {
            element.addEventListener('touchstart', () => {
                this.triggerHaptic('light');
            });
        });

        // Success actions get medium haptic
        document.addEventListener('click', (e) => {
            if (e.target.closest('.export-option, .btn-success')) {
                this.triggerHaptic('medium');
            }
        });
    }

    triggerHaptic(intensity = 'light') {
        // Try to use native haptic feedback if available
        if (navigator.vibrate) {
            const patterns = {
                light: [10],
                medium: [20],
                heavy: [30]
            };
            navigator.vibrate(patterns[intensity] || patterns.light);
        }
        
        // Visual feedback as fallback
        const target = event.target.closest('.btn, .nav-item, .template-option, .color-option');
        if (target) {
            target.classList.add(`haptic-${intensity}`);
            setTimeout(() => {
                target.classList.remove(`haptic-${intensity}`);
            }, 200);
        }
    }

    setupAutoSave() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('change', () => {
                    this.autoSaveForm(form);
                });
            });
        });
    }

    autoSaveForm(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem('autoSave_' + form.id || 'form', JSON.stringify({
            data: data,
            timestamp: Date.now()
        }));
        
        this.showAutoSaveIndicator();
    }

    showAutoSaveIndicator() {
        let indicator = document.getElementById('auto-save-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'auto-save-indicator';
            indicator.innerHTML = '<i class="fas fa-check"></i> Auto-saved';
            indicator.style.cssText = `
                position: fixed;
                top: 110px;
                right: 20px;
                background: var(--success-color);
                color: white;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 12px;
                z-index: 1050;
                opacity: 0;
                transform: translateY(-10px);
                transition: all 0.3s ease;
            `;
            document.body.appendChild(indicator);
        }
        
        indicator.style.opacity = '1';
        indicator.style.transform = 'translateY(0)';
        
        setTimeout(() => {
            indicator.style.opacity = '0';
            indicator.style.transform = 'translateY(-10px)';
        }, 2000);
    }

    setupPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        let isPulling = false;
        
        const mainContent = document.querySelector('.main-content');
        if (!mainContent) return;
        
        let refreshIndicator = document.createElement('div');
        refreshIndicator.className = 'pull-refresh';
        refreshIndicator.innerHTML = '<i class="fas fa-sync-alt"></i>';
        document.body.appendChild(refreshIndicator);
        
        mainContent.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                isPulling = true;
            }
        });
        
        mainContent.addEventListener('touchmove', (e) => {
            if (!isPulling) return;
            
            currentY = e.touches[0].clientY;
            pullDistance = currentY - startY;
            
            if (pullDistance > 0 && pullDistance < 100) {
                e.preventDefault();
                refreshIndicator.style.transform = `translateX(-50%) translateY(${pullDistance - 60}px)`;
                refreshIndicator.style.opacity = pullDistance / 100;
                
                if (pullDistance > 60) {
                    refreshIndicator.classList.add('visible');
                }
            }
        });
        
        mainContent.addEventListener('touchend', () => {
            if (isPulling && pullDistance > 60) {
                this.refreshPage();
            }
            
            isPulling = false;
            pullDistance = 0;
            refreshIndicator.classList.remove('visible');
            refreshIndicator.style.transform = 'translateX(-50%)';
            refreshIndicator.style.opacity = '0';
        });
    }

    refreshPage() {
        // Simulate refresh with actual page reload
        setTimeout(() => {
            window.location.reload();
        }, 500);
    }

    handleBackButton(event) {
        // Custom back button handling for SPA-like experience
        console.log('Back button pressed');
    }

    handleOnline() {
        this.showNotification('Back online', 'success');
    }

    handleOffline() {
        this.showNotification('You are offline', 'warning');
    }

    handleVisibilityChange() {
        if (document.hidden) {
            console.log('App went to background');
        } else {
            console.log('App came to foreground');
            // Check for updates when app returns to foreground
            this.checkForUpdates();
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification-toast`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'warning' ? 'exclamation-triangle' : 'info'}"></i>
            ${message}
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
        
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    initPWA() {
        // PWA functionality without install prompt
        window.addEventListener('appinstalled', () => {
            this.showNotification('App installed successfully!', 'success');
        });
    }

    checkForUpdates() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.ready.then(registration => {
                registration.update();
            });
        }
    }

    // Utility functions
    static loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    static loadStyle(href) {
        return new Promise((resolve, reject) => {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = resolve;
            link.onerror = reject;
            document.head.appendChild(link);
        });
    }
}

// Global utilities
window.CardApp = {
    showLoading: function(element) {
        if (element) {
            element.classList.add('loading');
        }
    },
    
    hideLoading: function(element) {
        if (element) {
            element.classList.remove('loading');
        }
    },
    
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                app.showNotification('Copied to clipboard!', 'success');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                app.showNotification('Copied to clipboard!', 'success');
            } catch (err) {
                console.error('Could not copy text: ', err);
            }
            document.body.removeChild(textArea);
        }
    }
};

// Add CSS for ripple animation
const rippleStyles = document.createElement('style');
rippleStyles.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyles);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new MobileCardApp();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileCardApp;
}
