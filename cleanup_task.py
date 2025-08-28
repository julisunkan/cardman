import os
import time
import threading
import glob
from datetime import datetime, timedelta

class FileCleanupManager:
    def __init__(self, export_folder='exports', preview_folder='static/previews', cleanup_interval=60):
        """
        Initialize cleanup manager
        
        Args:
            export_folder: Folder containing exported cards
            preview_folder: Folder containing preview images
            cleanup_interval: Time in seconds before files are deleted (default: 60 seconds)
        """
        self.export_folder = export_folder
        self.preview_folder = preview_folder
        self.cleanup_interval = cleanup_interval
        self.cleanup_thread = None
        self.running = False
        
    def start_cleanup_service(self):
        """Start the background cleanup service"""
        if not self.running:
            self.running = True
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
            self.cleanup_thread.start()
            print(f"Cleanup service started - files will be deleted after {self.cleanup_interval} seconds")
    
    def stop_cleanup_service(self):
        """Stop the cleanup service"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join()
            print("Cleanup service stopped")
    
    def _cleanup_loop(self):
        """Main cleanup loop that runs in background"""
        while self.running:
            try:
                self._cleanup_old_files()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Cleanup error: {e}")
                time.sleep(30)
    
    def _cleanup_old_files(self):
        """Remove files older than cleanup_interval"""
        current_time = time.time()
        cutoff_time = current_time - self.cleanup_interval
        
        # Clean export folder
        if os.path.exists(self.export_folder):
            for file_pattern in ['*.png', '*.pdf', '*.html', '*.zip']:
                files = glob.glob(os.path.join(self.export_folder, file_pattern))
                for file_path in files:
                    try:
                        if os.path.getmtime(file_path) < cutoff_time:
                            os.remove(file_path)
                            print(f"Deleted expired file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
        
        # Clean preview folder
        if os.path.exists(self.preview_folder):
            for file_pattern in ['*.png', '*.jpg', '*.jpeg']:
                files = glob.glob(os.path.join(self.preview_folder, file_pattern))
                for file_path in files:
                    try:
                        if os.path.getmtime(file_path) < cutoff_time:
                            os.remove(file_path)
                            print(f"Deleted expired preview: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")

# Global cleanup manager instance
cleanup_manager = FileCleanupManager()

def init_cleanup_service():
    """Initialize and start the cleanup service"""
    cleanup_manager.start_cleanup_service()

def stop_cleanup_service():
    """Stop the cleanup service"""
    cleanup_manager.stop_cleanup_service()