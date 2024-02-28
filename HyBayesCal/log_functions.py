import logging
from config import logfile_path

"""
File to record the log actions

"""

logging.basicConfig(filename=logfile_path, format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO)

def log_actions(func):
    """
    Author - Abhishek
    A decorator function for logging errors that occur during the execution of other functions.

    Parameters: func (function): The function being decorated.

    Returns: function: The wrapper function.
    """
    
    def wrapper(*args, **kwargs):
        """
        Wrapper function that executes the decorated function and logs any errors.

        Parameters: *args: Positional arguments passed to the decorated function.
            **kwargs: Keyword arguments passed to the decorated function.

        Returns: Any: The result of the decorated function.

        Raises: Exception: Any exception raised by the decorated function.
        """
        
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Error occurred in function {func.__name__}: {e}")
            raise
    return wrapper
