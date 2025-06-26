"""
Demo Logging Helper Module

Provides standardized logging setup for all demo scripts to ensure consistent
log formatting and output locations.
"""

import os
import sys
import logging
import datetime

def setup_demo_logger(demo_name, log_level=logging.INFO):
    """
    Set up standardized logging for demo scripts.
    
    Args:
        demo_name (str): Name of the demo for the log file and logger name
        log_level (int): Logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Ensure log directory exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    log_dir = os.path.join(parent_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{demo_name.lower().replace(' ', '_')}_{timestamp}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    # Configure logger
    logger = logging.getLogger(demo_name)
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Create file handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log setup information
    logger.info(f"Logging initialized for {demo_name}")
    logger.info(f"Log file: {log_path}")
    
    return logger

class DemoLogger:
    """Legacy compatibility class for older demo scripts"""
    
    def __init__(self, log_path=None, demo_name="Generic Demo"):
        self.logger = setup_demo_logger(demo_name)
        if log_path:
            self.logger.info(f"Note: Legacy log path '{log_path}' ignored; using standardized log location")
    
    def log(self, message, level="INFO"):
        """Log a message at the specified level"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO, 
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        log_level = level_map.get(level, logging.INFO)
        self.logger.log(log_level, message)

def print_and_log(logger, message, level="INFO"):
    """Print a message and log it (for backward compatibility)"""
    if isinstance(logger, DemoLogger):
        logger.log(message, level)
    else:
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO, 
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        log_level = level_map.get(level, logging.INFO)
        logger.log(log_level, message)
