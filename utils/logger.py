import logging
import os

# Ensure logs/ directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AMSLogger")

# Example usage
if __name__ == "__main__":
    logger.info("Logging is configured correctly.")
    logger.warning("This is a warning.")
    logger.error("This is an error log.")
