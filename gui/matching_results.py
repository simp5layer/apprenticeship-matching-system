from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt, QDateTime
from database.db_manager import DBManager
from models.student import Student
from models.opening import Opening
from models.matching import match_openings_for_student


class MatchingResultsWindow(QWidget):
    """
    Displays apprenticeship openings matched to a student,
    shows deadline status, allows the student to view details,
    apply or cancel an application, and navigate back.
    """
    def __init__(self, student_row):
        super().__init__()
        self.student_row = student_row
        self.db = DBManager()
        self.openings = []  # list of Opening objects
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Matching Apprenticeship Openings")
        self.setGeometry(300, 300, 600, 500)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        matches = self.get_matches()
        if not matches:
            QMessageBox.information(
                self,
                "No Matches",
                "No openings match your criteria."
            )

        # List to display matched openings with deadline status
        self.list_widget = QListWidget()
        # current time in ISO format for comparison
        # get a true datetime for “now”
        now_dt = datetime.utcnow()
        for opening in matches:
            base = f"{opening.name} @ {opening.location} — SAR {opening.stipend}"

            # figure out the deadline as a datetime
            dl = opening.deadline
            if isinstance(dl, str):
                try:
                    dl = datetime.fromisoformat(dl)
                except ValueError:
                    dl = None

            # open vs closed
            status = "Application Open"
            color  = Qt.GlobalColor.green
            if dl and dl < now_dt:
                status = "Application Closed"
                color  = Qt.GlobalColor.red

            display = f"{base}   [{status}]"
            item    = QListWidgetItem(display)
            item.setForeground(color)
            self.list_widget.addItem(item)
            self.openings.append(opening)

        # Double‑click to show details
        self.list_widget.itemDoubleClicked.connect(self.show_details)
        # Update toggle when selection changes
        self.list_widget.currentRowChanged.connect(lambda _: self.update_toggle_button())
        layout.addWidget(self.list_widget)

        # Apply / Cancel button
        self.toggle_btn = QPushButton()
        self.toggle_btn.clicked.connect(self.toggle_current_application)
        layout.addWidget(self.toggle_btn)

        # Back to dashboard
        back_btn = QPushButton("Back to Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard)
        layout.addWidget(back_btn)

        if self.openings:
            self.list_widget.setCurrentRow(0)
        self.update_toggle_button()

        self.setLayout(layout)

    def get_matches(self):
        # Build Student model
        prefs = (self.student_row['preferred_locations'].split(';')
                 if self.student_row['preferred_locations'] else [])
        skills = (self.student_row['skills'].split(',')
                  if self.student_row['skills'] else [])
        student = Student(
            student_id=self.student_row['student_id'],
            name=self.student_row['name'],
            email=self.student_row['email'],
            gpa=self.student_row['gpa'],
            specialization=self.student_row['specialization'],
            preferred_locations=prefs,
            skills=skills
        )
        # Fetch raw openings
        raw = self.db.get_openings_by_specialization(student.specialization)
        opening_list = []
        for row in raw:
            req_skills = row['required_skills'].split(',') if row['required_skills'] else []
            deadline_val = row['deadline'] if 'deadline' in row.keys() else None
            opening_list.append(Opening(
                opening_id=row['opening_id'],
                company_email=row['company_email'],
                name=row['opening_name'],
                specialization=row['specialization'],
                location=row['location'],
                stipend=row['stipend'],
                required_skills=req_skills,
                required_gpa=row['required_gpa'],
                priority=row['priority'],
                deadline=deadline_val
            ))
        return match_openings_for_student(student, opening_list)

    def show_details(self, item: QListWidgetItem):
        idx = self.list_widget.row(item)
        opening = self.openings[idx]
        info = (
            f"Opening ID: {opening.opening_id}\n"
            f"Name: {opening.name}\n"
            f"Specialization: {opening.specialization}\n"
            f"Location: {opening.location}\n"
            f"Stipend: SAR {opening.stipend}\n"
            f"Required GPA: {opening.required_gpa}\n"
            f"Priority: {opening.priority}\n"
            f"Required Skills: {', '.join(opening.required_skills)}\n"
            f"Deadline: {opening.deadline}"
        )
        QMessageBox.information(self, "Opening Details", info)

    def update_toggle_button(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            self.toggle_btn.setText("Select an opening to Apply/Cancel")
            self.toggle_btn.setEnabled(False)
            return
        self.toggle_btn.setEnabled(True)
        opening = self.openings[idx]
        applied = bool(self.db.cursor.execute(
            "SELECT 1 FROM applications WHERE student_email=? AND opening_id=?",
            (self.student_row['email'], opening.opening_id)
        ).fetchone())
        self.toggle_btn.setText("Cancel Application" if applied else "Apply")

    def toggle_current_application(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            return

        o = self.openings[idx]
        email = self.student_row['email']

        # --- New: block Apply if deadline has passed ---
        now = datetime.now()
        if self.toggle_btn.text() == "Apply" and o.deadline and now > o.deadline:
            QMessageBox.warning(
                self,
                "Application Closed",
                "Sorry, you cannot apply: the deadline for this opening has passed."
            )
            return

        # Proceed with normal apply/cancel logic
        if self.toggle_btn.text() == "Apply":
            if self.db.apply_to_opening(email, o.opening_id):
                QMessageBox.information(self, "Applied", "Your application was successful.")
        else:
            ans = QMessageBox.question(
                self, "Cancel Application",
                "Are you sure you want to cancel your application?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if ans == QMessageBox.StandardButton.Yes:
                self.db.cancel_application(email, o.opening_id)
                QMessageBox.information(self, "Cancelled", "Your application has been cancelled.")

        # Refresh the button text (“Apply” or “Cancel”) after the action
        self.update_toggle_button()
    def back_to_dashboard(self):
        from gui.student_dashboard import StudentDashboard
        self.next_window = StudentDashboard(self.student_row)
        self.next_window.show()
        self.close()
