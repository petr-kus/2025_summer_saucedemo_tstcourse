"""
Screenshot Helper Module
Utilities for capturing and managing screenshots during tests
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

from .logging_config import get_logger


class ScreenshotManager:
    """Manages screenshot capture and storage"""
    
    def __init__(self, screenshot_dir: str = "screenshots"):
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(exist_ok=True)
        self.logger = get_logger(self.__class__.__name__)
    
    def capture_screenshot(self, 
                         driver: WebDriver, 
                         test_name: str, 
                         step_name: str = "",
                         reason: str = "") -> str:
        """
        Capture screenshot with descriptive filename
        
        Args:
            driver: WebDriver instance
            test_name: Name of the test
            step_name: Current test step
            reason: Reason for screenshot (e.g., 'failure', 'verification')
            
        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # milliseconds
        
        # Create descriptive filename
        filename_parts = [test_name, timestamp]
        if step_name:
            filename_parts.insert(-1, step_name)
        if reason:
            filename_parts.insert(-1, reason)
        
        filename = "_".join(filename_parts) + ".png"
        filepath = self.screenshot_dir / filename
        
        try:
            # Capture screenshot
            driver.save_screenshot(str(filepath))
            self.logger.screenshot_taken(str(filepath), reason)
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {str(e)}")
            return ""
    
    def capture_on_failure(self, driver: WebDriver, test_name: str) -> str:
        """Capture screenshot on test failure"""
        return self.capture_screenshot(driver, test_name, "failure", "test_failed")
    
    def capture_for_verification(self, driver: WebDriver, test_name: str, verification: str) -> str:
        """Capture screenshot for verification step"""
        return self.capture_screenshot(driver, test_name, verification, "verification")
    
    def cleanup_old_screenshots(self, days_old: int = 7):
        """Remove screenshots older than specified days"""
        try:
            import time
            current_time = time.time()
            
            for screenshot in self.screenshot_dir.glob("*.png"):
                file_time = os.path.getctime(screenshot)
                if (current_time - file_time) > (days_old * 24 * 60 * 60):
                    screenshot.unlink()
                    self.logger.info(f"Removed old screenshot: {screenshot}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup screenshots: {str(e)}")


# Global screenshot manager instance
screenshot_manager = ScreenshotManager()


def capture_screenshot(driver: WebDriver, test_name: str, step_name: str = "", reason: str = "") -> str:
    """Convenience function to capture screenshot"""
    return screenshot_manager.capture_screenshot(driver, test_name, step_name, reason)