import sys
from PyQt6.QtWidgets import QApplication

# Import the entry window (role selection)
from gui.entry_window import EntryWindow

# Import database setup to ensure tables exist
from database import setup

# Import utility modules (if needed globally)
from utils import encryption, validation, notifications

# Import matching system (for business logic use within GUIs)
from models.matching import MatchingSystem

# Optional: Import logger (if you have a custom logger)
# from utils.logger import setup_logger


def main():
    # Step 1: Initialize database (creates tables if not existing)
    setup.create_tables()

    # Step 2: Initialize the QApplication
    app = QApplication(sys.argv)

    # Step 3: Launch the Entry Window for role selection
    entry_window = EntryWindow()
    entry_window.show()

    # Step 4: Execute the app loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
