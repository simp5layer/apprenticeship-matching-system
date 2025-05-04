# gui/student_dashboard.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class StudentDashboard(QWidget):
    def __init__(self, user_row):
        """
        user_row: sqlite3.Row or dict with keys:
          'name', 'student_id', 'gpa', 'specialization',
          'preferred_locations', 'skills', 'email'
        """
        super().__init__()
        self.user = user_row
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Student Dashboard — {self.user['name']}")
        self.setGeometry(250, 250, 600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Profile summary
        layout.addWidget(QLabel(f"Welcome, {self.user['name']}!"))
        layout.addWidget(QLabel(f"GPA: {self.user['gpa']}"))
        layout.addWidget(QLabel(f"Specialization: {self.user['specialization']}"))
        prefs = self.user['preferred_locations'].replace(';', ', ')
        layout.addWidget(QLabel(f"Preferred Locations: {prefs}"))

                # View matches button
        btn_view_matches = QPushButton("View Matching Results")
        btn_view_matches.clicked.connect(self.show_matches)
        layout.addWidget(btn_view_matches)

        # Edit profile button
        btn_edit = QPushButton("Edit Profile")
        btn_edit.clicked.connect(self.edit_profile)
        layout.addWidget(btn_edit)

        # Log out button
        btn_logout = QPushButton("Log Out")
        btn_logout.clicked.connect(self.log_out)
        layout.addWidget(btn_logout)

        self.setLayout(layout)

    def show_matches(self):
        from gui.matching_results import MatchingResultsWindow
        self.next_window = MatchingResultsWindow(self.user)
        self.next_window.show()
        self.close()

    def edit_profile(self):
        from gui.student_profile_window import StudentProfileWindow
        self.next_window = StudentProfileWindow(self.user['email'])
        self.next_window.show()
        self.close()

    def log_out(self):
        from gui.login_window import LoginWindow
        self.next_window = LoginWindow(role='student')
        self.next_window.show()
        self.close()
