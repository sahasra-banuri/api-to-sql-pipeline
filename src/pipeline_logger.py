import logging
from pathlib import Path


def setup_logger():

    # Create logs directory
    log_folder = Path("logs")
    log_folder.mkdir(parents=True, exist_ok=True)

    # Define log file
    log_file = log_folder / "pipeline.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )

    logging.getLogger("mysql.connector").setLevel(logging.WARNING)

    return logging.getLogger("data_pipeline")