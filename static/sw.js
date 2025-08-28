// Service Worker for CardGen PWA
const CACHE_NAME = 'cardgen-v1.0.0';
const urlsToCache = [
    '/',
    '/create',
    '/preview',
    '/batch',
    '/static/css/style.css',
    '/static/css/mobile.css',
    '/static/js/app.js',
    '/static/js/templates.js',
    '/static/js/card-preview.js',
    '/static/manifest.json',
    // External dependencies
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
];

// Install event - cache resources
self.addEventListener('install', event => {
    console.log('Service Worker installing');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Caching app shell');
                return cache.addAll(urlsToCache.map(url => {
                    return new Request(url, { mode: 'cors' });
                }));
            })
            .catch(error => {
                console.error('Error caching resources:', error);
                // Continue installation even if some resources fail to cache
                return caches.open(CACHE_NAME);
            })
    );
    
    // Force the waiting service worker to become the active service worker
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activating');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    // Claim control of all open pages
    return self.clients.claim();
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', event => {
    const request = event.request;
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip chrome-extension and other non-http requests
    if (!request.url.startsWith('http')) {
        return;
    }
    
    event.respondWith(
        caches.match(request)
            .then(response => {
                // Return cached version if available
                if (response) {
                    // For HTML pages, try to fetch updated version in background
                    if (request.headers.get('accept')?.includes('text/html')) {
                        fetchAndCache(request);
                    }
                    return response;
                }
                
                // Fetch from network
                return fetchAndCache(request);
            })
            .catch(() => {
                // Network failed, return offline page for HTML requests
                if (request.headers.get('accept')?.includes('text/html')) {
                    return caches.match('/') || createOfflinePage();
                }
                
                // For other requests, return a basic response
                return new Response('Offline', { 
                    status: 503,
                    statusText: 'Service Unavailable'
                });
            })
    );
});

// Helper function to fetch and cache resources
function fetchAndCache(request) {
    return fetch(request)
        .then(response => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
            }
            
            // Clone the response
            const responseToCache = response.clone();
            
            // Cache successful responses
            caches.open(CACHE_NAME)
                .then(cache => {
                    cache.put(request, responseToCache);
                })
                .catch(error => {
                    console.error('Error caching response:', error);
                });
            
            return response;
        });
}

// Create a basic offline page
function createOfflinePage() {
    const offlineHTML = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Offline - CardGen</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 2rem;
                    text-align: center;
                    background: #f8fafc;
                    color: #1e293b;
                }
                .offline-container {
                    max-width: 400px;
                    margin: 2rem auto;
                    padding: 2rem;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .offline-icon {
                    font-size: 4rem;
                    margin-bottom: 1rem;
                }
                h1 {
                    margin-bottom: 1rem;
                    color: #374151;
                }
                p {
                    margin-bottom: 1.5rem;
                    color: #6b7280;
                }
                .retry-btn {
                    background: #2563eb;
                    color: white;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1rem;
                }
                .retry-btn:hover {
                    background: #1d4ed8;
                }
            </style>
        </head>
        <body>
            <div class="offline-container">
                <div class="offline-icon">📱</div>
                <h1>You're Offline</h1>
                <p>CardGen is not available right now. Please check your internet connection and try again.</p>
                <button class="retry-btn" onclick="window.location.reload()">
                    Try Again
                </button>
            </div>
        </body>
        </html>
    `;
    
    return new Response(offlineHTML, {
        headers: { 'Content-Type': 'text/html' }
    });
}

// Background sync for form submissions
self.addEventListener('sync', event => {
    if (event.tag === 'card-data-sync') {
        event.waitUntil(syncCardData());
    } else if (event.tag === 'batch-sync') {
        event.waitUntil(syncBatchData());
    }
});

// Sync card data when online
async function syncCardData() {
    try {
        // Get pending card data from IndexedDB
        const pendingData = await getPendingData('cardData');
        
        if (pendingData.length > 0) {
            for (const data of pendingData) {
                try {
                    const response = await fetch('/save_card_data', {
                        method: 'POST',
                        body: data.formData
                    });
                    
                    if (response.ok) {
                        await removePendingData('cardData', data.id);
                    }
                } catch (error) {
                    console.error('Error syncing card data:', error);
                }
            }
        }
    } catch (error) {
        console.error('Error in card data sync:', error);
    }
}

// Sync batch data when online
async function syncBatchData() {
    try {
        const pendingBatches = await getPendingData('batchData');
        
        if (pendingBatches.length > 0) {
            for (const batch of pendingBatches) {
                try {
                    const response = await fetch('/batch_process', {
                        method: 'POST',
                        body: batch.formData
                    });
                    
                    if (response.ok) {
                        await removePendingData('batchData', batch.id);
                    }
                } catch (error) {
                    console.error('Error syncing batch data:', error);
                }
            }
        }
    } catch (error) {
        console.error('Error in batch data sync:', error);
    }
}

// IndexedDB helpers for offline storage
function getPendingData(store) {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('CardGenOffline', 1);
        
        request.onerror = () => reject(request.error);
        
        request.onsuccess = () => {
            const db = request.result;
            if (!db.objectStoreNames.contains(store)) {
                resolve([]);
                return;
            }
            
            const transaction = db.transaction([store], 'readonly');
            const objectStore = transaction.objectStore(store);
            const getAllRequest = objectStore.getAll();
            
            getAllRequest.onsuccess = () => resolve(getAllRequest.result);
            getAllRequest.onerror = () => reject(getAllRequest.error);
        };
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('cardData')) {
                db.createObjectStore('cardData', { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains('batchData')) {
                db.createObjectStore('batchData', { keyPath: 'id', autoIncrement: true });
            }
        };
    });
}

function removePendingData(store, id) {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('CardGenOffline', 1);
        
        request.onerror = () => reject(request.error);
        
        request.onsuccess = () => {
            const db = request.result;
            const transaction = db.transaction([store], 'readwrite');
            const objectStore = transaction.objectStore(store);
            const deleteRequest = objectStore.delete(id);
            
            deleteRequest.onsuccess = () => resolve();
            deleteRequest.onerror = () => reject(deleteRequest.error);
        };
    });
}

// Push notification handling
self.addEventListener('push', event => {
    const options = {
        body: 'Your business cards are ready for download!',
        icon: '/static/icon-192x192.png',
        badge: '/static/icon-192x192.png',
        data: {
            url: '/preview'
        },
        actions: [
            {
                action: 'open',
                title: 'Open App'
            },
            {
                action: 'dismiss',
                title: 'Dismiss'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('CardGen', options)
    );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'open' || !event.action) {
        event.waitUntil(
            clients.matchAll().then(clientList => {
                // If app is already open, focus it
                for (const client of clientList) {
                    if (client.url.includes(self.location.origin) && 'focus' in client) {
                        return client.focus();
                    }
                }
                
                // Otherwise, open new window
                if (clients.openWindow) {
                    return clients.openWindow(event.notification.data?.url || '/');
                }
            })
        );
    }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', event => {
    if (event.tag === 'cleanup') {
        event.waitUntil(cleanupOldCache());
    }
});

// Clean up old cached data
async function cleanupOldCache() {
    try {
        const cache = await caches.open(CACHE_NAME);
        const requests = await cache.keys();
        const now = Date.now();
        
        for (const request of requests) {
            // Remove preview images older than 24 hours
            if (request.url.includes('/static/previews/')) {
                const response = await cache.match(request);
                if (response) {
                    const dateHeader = response.headers.get('date');
                    if (dateHeader) {
                        const responseDate = new Date(dateHeader);
                        const ageInHours = (now - responseDate.getTime()) / (1000 * 60 * 60);
                        
                        if (ageInHours > 24) {
                            await cache.delete(request);
                        }
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error cleaning up cache:', error);
    }
}

// Message handling from main app
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({ version: CACHE_NAME });
    }
    
    if (event.data && event.data.type === 'CACHE_PREVIEW') {
        const { url } = event.data;
        if (url) {
            caches.open(CACHE_NAME).then(cache => {
                cache.add(url);
            });
        }
    }
});

console.log('Service Worker loaded and ready');
