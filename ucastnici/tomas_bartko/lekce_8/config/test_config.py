"""
Test Configuration Module
Centralized configuration for SauceDemo test framework
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class Environment(Enum):
    """Test environments"""
    STAGING = "staging"
    PRODUCTION = "production"


class Browser(Enum):
    """Supported browsers"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"


class UserType(Enum):
    """SauceDemo user types with their credentials"""
    STANDARD = ("standard_user", "secret_sauce")
    PROBLEM = ("problem_user", "secret_sauce")
    PERFORMANCE_GLITCH = ("performance_glitch_user", "secret_sauce")
    ERROR = ("error_user", "secret_sauce")
    VISUAL = ("visual_user", "secret_sauce")
    LOCKED_OUT = ("locked_out_user", "secret_sauce")
    INVALID = ("invalid_user", "wrong_password")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


@dataclass
class TestConfig:
    """Main test configuration"""
    
    # Browser settings
    browser: Browser = Browser.CHROME
    headless: bool = True
    window_size: str = "1920,1080"
    
    # Timeouts
    implicit_wait: int = 10
    explicit_wait: int = 15
    page_load_timeout: int = 30
    
    # URLs
    base_url: str = "https://www.saucedemo.com/"
    
    # Test data
    default_user: UserType = UserType.STANDARD
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Screenshots
    screenshot_on_failure: bool = True
    screenshot_dir: str = "screenshots"
    
    # Reports
    html_report_dir: str = "reports"
    allure_results_dir: str = "allure-results"


class TestData:
    """Test data constants"""
    
    # Product names for testing
    PRODUCT_NAMES = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light", 
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]
    
    # Expected error messages
    ERROR_MESSAGES = {
        "invalid_credentials": "Epic sadface: Username and password do not match any user in this service",
        "locked_out_user": "Epic sadface: Sorry, this user has been locked out.",
        "empty_username": "Epic sadface: Username is required",
        "empty_password": "Epic sadface: Password is required"
    }
    
    # Shopping cart test data
    SHOPPING_SCENARIOS = {
        "single_item": 1,
        "multiple_items": 3,
        "full_cart": 6
    }


# Global config instance
config = TestConfig()


def get_config() -> TestConfig:
    """Get current test configuration"""
    return config


def set_environment_from_env_vars():
    """Set configuration from environment variables"""
    if os.getenv("HEADLESS"):
        config.headless = os.getenv("HEADLESS").lower() == "true"
    
    if os.getenv("BROWSER"):
        try:
            config.browser = Browser(os.getenv("BROWSER").lower())
        except ValueError:
            pass
    
    if os.getenv("BASE_URL"):
        config.base_url = os.getenv("BASE_URL")


# Initialize from environment on import
set_environment_from_env_vars()