"""
Logging Configuration Module
Advanced logging setup for test framework
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class TestLogger:
    """Advanced test logger with context and structured logging"""
    
    def __init__(self, name: str, log_level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup console and file handlers"""
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"test_run_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def test_step(self, step_description: str, **kwargs):
        """Log a test step with context"""
        context = f" | Context: {kwargs}" if kwargs else ""
        self.logger.info(f"🔸 STEP: {step_description}{context}")
    
    def test_action(self, action: str, element: str = "", value: str = ""):
        """Log a test action"""
        details = f" on '{element}'" if element else ""
        details += f" with value '{value}'" if value else ""
        self.logger.info(f"🔹 ACTION: {action}{details}")
    
    def test_verification(self, description: str, expected: str, actual: str, passed: bool):
        """Log a verification step"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.logger.info(f"🔍 VERIFY: {description} | Expected: '{expected}' | Actual: '{actual}' | {status}")
    
    def test_data(self, data_type: str, data: dict):
        """Log test data"""
        self.logger.info(f"📊 DATA: {data_type} | {data}")
    
    def screenshot_taken(self, path: str, reason: str = ""):
        """Log screenshot capture"""
        reason_text = f" - {reason}" if reason else ""
        self.logger.info(f"📸 SCREENSHOT: {path}{reason_text}")
    
    def error(self, message: str, exception: Optional[Exception] = None):
        """Log error with optional exception"""
        if exception:
            self.logger.error(f"❌ ERROR: {message} | Exception: {str(exception)}")
        else:
            self.logger.error(f"❌ ERROR: {message}")
    
    def warning(self, message: str):
        """Log warning"""
        self.logger.warning(f"⚠️  WARNING: {message}")
    
    def info(self, message: str):
        """Log info"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug"""
        self.logger.debug(f"🐛 DEBUG: {message}")


def get_logger(name: str, log_level: str = "INFO") -> TestLogger:
    """Get a configured test logger"""
    return TestLogger(name, log_level)