# gui/applicants_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager

class ApplicantsWindow(QWidget):
    """Window showing all applicants for a specific opening."""
    def __init__(self, opening_row):
        super().__init__()
        self.opening = opening_row
        self.db = DBManager()
        self.applicants = []
        self.init_ui()

    def init_ui(self):
        """Builds the UI: list of applicants and back button."""
        self.setWindowTitle(f"Applicants for “{self.opening['opening_name']}”")
        self.setGeometry(300, 300, 500, 450)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create the list widget BEFORE we ever try to use it
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.show_details)

        # Fetch & filter applicants
        raw = self.db.get_applicants_by_opening(self.opening['opening_id'])
        filtered = [
            s for s in raw
            if float(s['gpa']) >= self.opening['required_gpa']
               and self.opening['location'] in (s['preferred_locations'] or '').split(';')
        ]

        # Sort according to priority
        if self.opening['priority'] == 'location':
            loc = self.opening['location']
            buckets = {0: [], 1: [], 2: [], 3: []}
            for s in filtered:
                prefs = (s['preferred_locations'] or '').split(';')
                idx = prefs.index(loc) if loc in prefs else 3
                buckets[idx].append(s)
            ordered = []
            # within each bucket, sort by GPA descending
            for i in (0, 1, 2, 3):
                bucket_sorted = sorted(buckets[i], key=lambda s: -float(s['gpa']))
                ordered.extend(bucket_sorted)
        else:
            ordered = sorted(filtered, key=lambda s: -float(s['gpa']))

        if not ordered:
            QMessageBox.information(self, "No Applicants", "No one has applied yet.")

        # Populate the list widget and build applicants list
        for s in ordered:
            text = f"{s['name']}  •  GPA: {s['gpa']}  •  prefs: {s['preferred_locations']}"
            self.list_widget.addItem(QListWidgetItem(text))
            self.applicants.append(s)

        layout.addWidget(QLabel("Applicants:"))
        layout.addWidget(self.list_widget)

        # Back button
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignRight)
        back_btn = QPushButton("Back to Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard)
        btn_row.addWidget(back_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def show_details(self, item: QListWidgetItem):
        """Show a detailed info dialog for the double-clicked applicant."""
        idx = self.list_widget.row(item)
        row = self.applicants[idx]
        details = (
            f"Student ID: {row['student_id']}\n"
            f"Name: {row['name']}\n"
            f"Email: {row['email']}\n"
            f"Mobile: {row['mobile_number']}\n"
            f"GPA: {row['gpa']}\n"
            f"Specialization: {row['specialization']}\n"
            f"Preferred Locations: {row['preferred_locations']}\n"
            f"Skills: {row['skills']}"
        )
        QMessageBox.information(self, "Applicant Details", details)

    def back_to_dashboard(self):
        from gui.company_dashboard import CompanyDashboard
        user = self.db.get_user(self.opening['company_email'])
        self.next_window = CompanyDashboard(user, opening_id=self.opening['opening_id'])
        self.next_window.show()
        self.close()
