import logging
from config import logfile_path

logging.basicConfig(filename=logfile_path, format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)

def log_actions(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Error occurred in function {func.__name__}: {e}")
            raise
    return wrapper
