# gui/opening_name_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class OpeningNameWindow(QWidget):
    def __init__(self, company_email):
        super().__init__()
        self.company_email = company_email
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Name Your Apprenticeship Opening")
        self.setGeometry(300, 300, 500, 150)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Enter the name of your apprenticeship opening:"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Software Engineering Intern")
        layout.addWidget(self.name_input)

        back_btn = QPushButton("Back to Openings")
        back_btn.clicked.connect(self.back_to_list)
        layout.addWidget(back_btn)

        next_btn = QPushButton("Next ▶")
        next_btn.clicked.connect(self.handle_next)
        layout.addWidget(next_btn)

        self.setLayout(layout)

    def back_to_list(self):
        from gui.openings_list_window import OpeningsListWindow
        self.next_window = OpeningsListWindow({'email': self.company_email, 'role': 'company'})
        self.next_window.show()
        self.close()

    def handle_next(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Required", "Please enter a name for your opening.")
            return

        from gui.opening_details_window import OpeningDetailsWindow
        # keep a persistent reference so the window isn't garbage-collected
        self.next_window = OpeningDetailsWindow(self.company_email, name)
        self.next_window.show()
        self.close()
