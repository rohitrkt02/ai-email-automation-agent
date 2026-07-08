import os
import logging
from logging.handlers import RotatingFileHandler

def setup_agent_logger():
    """
    Sets up a production-grade rotating logging engine.
    As per Phase 13 Roadmap Requirements.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logs_dir = os.path.join(base_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file_path = os.path.join(logs_dir, 'agent_pipeline.log')
    
    # Create logger instance
    logger = logging.getLogger("EmailAgentLogger")
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if re-initialized
    if not logger.handlers:
        # Standard industrial logging format: Time - Module - Level - Message
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] -> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. File Handler (Auto-rotates when file reaches 5MB, keeps max 3 backups)
        file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # 2. Console Handler for live terminal output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Add both streams to central logger hook
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Global instance initialization
agent_logger = setup_agent_logger()