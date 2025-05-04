# gui/entry_window.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from gui.login_window import LoginWindow

class EntryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window settings
        self.setWindowTitle("Welcome")
        self.setGeometry(200, 200, 400, 200)

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Prompt label
        label = QLabel("Do you want to login or register as a:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Buttons for role selection
        button_layout = QHBoxLayout()
        self.company_button = QPushButton("Company")
        self.student_button = QPushButton("Student")

        # Connect clicks to open login window with role
        self.company_button.clicked.connect(lambda: self.open_login('company'))
        self.student_button.clicked.connect(lambda: self.open_login('student'))

        button_layout.addWidget(self.company_button)
        button_layout.addWidget(self.student_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def open_login(self, role: str):
        # Instantiate and show the login/register window with the selected role
        self.login_window = LoginWindow(role=role)
        self.login_window.show()
        self.close()
