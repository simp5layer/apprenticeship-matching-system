import logging  # Python's built-in logging library
import os  # Used for interacting with the file system

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure the logging settings to output to both a file and the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),  # Log to a file
        logging.StreamHandler()               # Also print to the terminal
    ]
)

# Create a logger instance named "AMSLogger"
logger = logging.getLogger("AMSLogger")

# Example test logs for verification when running directly
if __name__ == "__main__":
    logger.info("Logging is configured correctly.")
    logger.warning("This is a warning.")
    logger.error("This is an error log.")
