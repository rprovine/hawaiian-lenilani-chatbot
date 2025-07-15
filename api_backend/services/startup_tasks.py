"""
Startup tasks for the application
Ensures required directories exist
"""
import os
import logging

logger = logging.getLogger(__name__)


def ensure_directories_exist():
    """Create required directories if they don't exist"""
    directories = [
        "logs",
        "logs/leads"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"✅ Ensured directory exists: {directory}")
            
            # Verify it was created
            if os.path.exists(directory):
                logger.info(f"✅ Confirmed directory exists: {directory}")
            else:
                logger.error(f"❌ Failed to create directory: {directory}")
        except Exception as e:
            logger.error(f"❌ Error creating directory {directory}: {str(e)}")
            # Try to understand the error better
            try:
                # Check if parent exists
                parent = os.path.dirname(directory)
                if parent and not os.path.exists(parent):
                    logger.error(f"Parent directory doesn't exist: {parent}")
                
                # Check permissions
                if os.path.exists(parent or '.'):
                    logger.info(f"Parent directory permissions: {oct(os.stat(parent or '.').st_mode)}")
            except Exception as debug_e:
                logger.error(f"Debug error: {str(debug_e)}")


def run_startup_tasks():
    """Run all startup tasks"""
    logger.info("🚀 Running startup tasks...")
    ensure_directories_exist()
    logger.info("✅ Startup tasks completed")