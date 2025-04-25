from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from gui.matching_results import MatchingResultsWindow

class StudentDashboard(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Student Dashboard — {self.user['name']}")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Welcome, {self.user['name']}!"))
        btn_view_matches = QPushButton("View Matching Results")
        btn_view_matches.clicked.connect(self.show_matches)
        layout.addWidget(btn_view_matches)
        self.setLayout(layout)

    def show_matches(self):
        win = MatchingResultsWindow(self.user)
        win.show()
