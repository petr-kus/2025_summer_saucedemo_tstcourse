import logging
import os

def pytest_configure(config):
    logger = logging.getLogger("moje_testy")
    
    # Vyhneme se duplikaci handlerů
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')

    file_handler = logging.FileHandler(os.path.abspath("my_log.log"), mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)