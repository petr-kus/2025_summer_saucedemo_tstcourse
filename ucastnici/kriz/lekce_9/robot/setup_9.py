import logging
import logging
import os
import shutil

def setup_logger():
    logger = logging.getLogger("moje_testy")
    logger.setLevel(logging.DEBUG)   
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(os.path.abspath("my_log.log"), mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

screenshots_dir = "screenshots"
if os.path.exists(screenshots_dir):
    shutil.rmtree(screenshots_dir)
os.makedirs(screenshots_dir, exist_ok=True)
url = "https://www.saucedemo.com/"
logger = setup_logger()
logger = logging.getLogger("moje_testy")
logger.info("Logger nastaven.")