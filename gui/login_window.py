# gui/login_window.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager
from utils.validation import is_valid_email
from utils.encryption import hash_password, check_password
import random, string

class LoginWindow(QWidget):
    def __init__(self, role: str):
        super().__init__()
        self.role = role  # 'student' or 'company'
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        # Window title
        title_role = self.role.title()
        self.setWindowTitle(f"Login / Register ({title_role})")
        self.setGeometry(250, 250, 400, 350)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Prompt
        prompt = QLabel(f"Enter your credentials as {title_role}:")
        prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(prompt)

        # Email input
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")
        layout.addWidget(self.email_input)

        # Password input
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Buttons: Login and Register
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        layout.addLayout(btn_layout)

        # Forgot password link
        self.forgot_btn = QPushButton("Forgot Password?")
        self.forgot_btn.clicked.connect(self.handle_password_recovery)
        layout.addWidget(self.forgot_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Switch role button
        switch_text = "Switch to Student" if self.role == 'company' else "Switch to Company"
        self.switch_btn = QPushButton(switch_text)
        self.switch_btn.clicked.connect(self.switch_role)
        layout.addWidget(self.switch_btn)

        # Connect signals
        self.login_btn.clicked.connect(self.handle_login)
        self.register_btn.clicked.connect(self.handle_register)

        self.setLayout(layout)

    def switch_role(self):
        # Toggle between student and company login/register
        new_role = 'student' if self.role == 'company' else 'company'
        from gui.login_window import LoginWindow  # avoid circular
        self.next_window = LoginWindow(role=new_role)
        self.next_window.show()
        self.close()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if not is_valid_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return
        if not password:
            QMessageBox.warning(self, "Empty Password", "Please enter your password.")
            return
        user = self.db.get_user(email)
        if not user or user['role'] != self.role:
            QMessageBox.warning(self, "Login Failed", f"No {self.role} account for that email.")
            return
        if not check_password(password, user['hashed_password']):
            QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            return

        self.db.log_access(email)
        self.db.log_session(email, login=True)

        # Route to next window
        if self.role == 'company':
            from gui.openings_list_window import OpeningsListWindow
            self.next_window = OpeningsListWindow(user)
        else:
            # student: check if profile exists
            profile = self.db.get_student_by_email(email)
            if profile:
                from gui.student_dashboard import StudentDashboard
                self.next_window = StudentDashboard(profile)
            else:
                from gui.student_profile_window import StudentProfileWindow
                self.next_window = StudentProfileWindow(email)
        self.next_window.show()
        self.close()

    def handle_register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        # Validate inputs
        if not is_valid_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return
        if len(password) < 8 or not (any(c.isdigit() for c in password) and any(c.isalpha() for c in password)):
            QMessageBox.warning(self, "Weak Password", 
                "Password must be at least 8 characters and alphanumeric.")
            return
        if self.db.get_user(email):
            QMessageBox.warning(self, "Already Registered", "An account with that email already exists.")
            return
        # Create user
        hashed = hash_password(password)
        self.db.insert_user({
            "email": email,
            "hashed_password": hashed,
            "role": self.role
        })
        QMessageBox.information(self, "Registered", "Account created successfully!")

        # Next flow after register
        if self.role == 'company':
            from gui.opening_name_window import OpeningNameWindow
            self.next_window = OpeningNameWindow(email)
        else:
            from gui.student_profile_window import StudentProfileWindow
            self.next_window = StudentProfileWindow(email)
        self.next_window.show()
        self.close()

    def handle_password_recovery(self):
        # existing recovery logic
        pass
