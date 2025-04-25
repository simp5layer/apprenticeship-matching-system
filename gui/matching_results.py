from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from models.matching import MatchingSystem

class MatchingResultsWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.matcher = MatchingSystem()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Matching Results")
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Student Name", "GPA", "Opening", "Location", "Stipend"
        ])
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_matches()

    def load_matches(self):
        matches = self.matcher.match_students_to_openings(student=self.user)
        self.table.setRowCount(len(matches))
        for i, m in enumerate(matches):
            self.table.setItem(i, 0, QTableWidgetItem(m["student_name"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(m["gpa"])))
            self.table.setItem(i, 2, QTableWidgetItem(m["opening"]))
            self.table.setItem(i, 3, QTableWidgetItem(m["location"]))
            self.table.setItem(i, 4, QTableWidgetItem(str(m["stipend"])))
