from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager
from utils.validation import is_valid_email
from utils.encryption import hash_password, check_password

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login / Register")
        form = QFormLayout()
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Email:", self.email)
        form.addRow("Password:", self.password)

        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")
        self.feedback = QLabel()

        self.login_btn.clicked.connect(self.handle_login)
        self.register_btn.clicked.connect(self.handle_register)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.login_btn)
        vbox.addWidget(self.register_btn)
        vbox.addWidget(self.feedback)
        self.setLayout(vbox)

    def handle_login(self):
        email = self.email.text().strip()
        pwd = self.password.text()
        if not email or not pwd:
            self.feedback.setText("All fields are required.")
            return
        if not is_valid_email(email):
            self.feedback.setText("Invalid email format.")
            return

        user = self.db.get_user_by_email(email)
        if not user:
            self.feedback.setText("Email not registered.")
            return
        if not check_password(pwd, user["password"]):
            self.feedback.setText("Wrong password.")
            return

        role = user["role"]
        if role == "student":
            from gui.student_dashboard import StudentDashboard
            win = StudentDashboard(user)
        elif role == "company":
            from gui.company_dashboard import CompanyDashboard
            win = CompanyDashboard(user)
        else:
            from gui.admin_dashboard import AdminDashboard
            win = AdminDashboard()
        win.show()
        self.close()

    def handle_register(self):
        QMessageBox.information(self, "Register", "Registration flow not yet implemented.")
