# gui/company_dashboard.py

from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QMessageBox, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QDateTime
from database.db_manager import DBManager
from gui.openings_list_window import OpeningsListWindow

class CompanyDashboard(QWidget):
    """
    Main dashboard for a company: lets the user edit an existing opening's
    details (including deadline), return to the openings list, or view matches.
    """
    def __init__(self, user: dict, opening_id: int):
        super().__init__()
        self.user = user
        self.opening_id = opening_id
        self.db = DBManager()
        # Fetch the opening record from the database
        # Fetch the opening record (as sqlite3.Row)
        self.opening = self.db.get_opening_by_id(opening_id)
        # Convert to plain dict so .get() is available
        try:
            self.opening = dict(self.opening)
        except Exception:
            pass
        self.init_ui()

    def init_ui(self):
        """Builds the form layout and populates fields with current opening data."""
        self.setWindowTitle(f"Company Dashboard – {self.user['email']}")
        self.setGeometry(300, 300, 600, 450)

        form = QFormLayout()

        # Opening Name
        self.name_input = QLineEdit(self.opening['opening_name'])
        form.addRow(QLabel("Opening Name:"), self.name_input)

        # Specialization (dropdown)
        self.spec_combo = QComboBox()
        specs = [
            "Software Engineering", "Electrical Engineering", "Mechanical Engineering",
            "Civil Engineering", "Chemical Engineering", "Nuclear Engineering",
            "Industrial Engineering", "Mining Engineering"
        ]
        self.spec_combo.addItems(specs)
        # Pre-select saved specialization
        if self.opening['specialization'] in specs:
            idx = specs.index(self.opening['specialization'])
            self.spec_combo.setCurrentIndex(idx)
        form.addRow(QLabel("Specialization:"), self.spec_combo)

        # Location
        self.loc_input = QLineEdit(self.opening['location'])
        form.addRow(QLabel("Location:"), self.loc_input)

        # Stipend
        self.stip_input = QLineEdit(str(self.opening['stipend']))
        form.addRow(QLabel("Stipend (SAR):"), self.stip_input)

        # Required GPA
        # Use direct indexing on sqlite3.Row for required_gpa
        gpa_val = self.opening['required_gpa'] if 'required_gpa' in self.opening.keys() else 0
        self.gpa_input = QLineEdit(str(gpa_val))
        form.addRow(QLabel("Required GPA (0–5):"), self.gpa_input)

        # Priority (dropdown with display vs stored data)
        self.priority_combo = QComboBox()
        self.priority_combo.addItem("Location", "location")
        self.priority_combo.addItem("GPA",      "gpa")
        # Pre-select saved priority
        current_priority = self.opening.get('priority', 'location')
        for i in range(self.priority_combo.count()):
            if self.priority_combo.itemData(i) == current_priority:
                self.priority_combo.setCurrentIndex(i)
                break
        form.addRow(QLabel("Priority:"), self.priority_combo)

        # Deadline picker (with millisecond precision)
        self.deadline_edit = QDateTimeEdit()
        self.deadline_edit.setCalendarPopup(True)
        saved = self.opening.get("deadline")
        if saved:
            # first try ISO-with-ms
            dt = QDateTime.fromString(saved, Qt.DateFormat.ISODateWithMs)
            if not dt.isValid():
                # fallback to plain ISO
                dt = QDateTime.fromString(saved, Qt.DateFormat.ISODate)
            self.deadline_edit.setDateTime(dt if dt.isValid()
                                           else QDateTime.currentDateTime().addDays(7))
        else:
            # default one week out
            self.deadline_edit.setDateTime(QDateTime.currentDateTime().addDays(7))
        form.addRow(QLabel("Deadline:"), self.deadline_edit)

        # Required Skills
        self.skills_input = QTextEdit(self.opening['required_skills'])
        form.addRow(QLabel("Required Skills:"), self.skills_input)

        # Buttons
        btn_save = QPushButton("Save Changes")
        btn_save.clicked.connect(self.handle_save)
        form.addRow(btn_save)

        btn_back = QPushButton("Back to Openings")
        btn_back.clicked.connect(self.back_to_openings)
        form.addRow(btn_back)

        btn_view = QPushButton("View Matches")
        btn_view.clicked.connect(self.view_matches)
        form.addRow(btn_view)

        self.setLayout(form)

    def handle_save(self):
        """
        Validate inputs, collect updated values (including deadline as ISO string),
        then call DBManager.update_opening and show a confirmation.
        """
        # Gather and validate all fields
        name = self.name_input.text().strip()
        location = self.loc_input.text().strip()
        stipend_text = self.stip_input.text().strip()
        gpa_text = self.gpa_input.text().strip()
        skills = self.skills_input.toPlainText().strip()
        priority = self.priority_combo.currentData()
        # Serialize deadline *with* milliseconds so it round‐trips correctly
        # preserve millisecond precision so we can re-load it unchanged
        deadline_iso = self.deadline_edit.dateTime().toString(
            Qt.DateFormat.ISODateWithMs
        )
        


        if not (name and location and stipend_text and gpa_text and skills):
            QMessageBox.warning(self, "Missing Fields", "All fields are required.")
            return

        try:
            stipend = float(stipend_text)
            if stipend <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Stipend", "Stipend must be > 0.")
            return

        try:
            req_gpa = float(gpa_text)
            if not (0 <= req_gpa <= 5):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid GPA", "GPA must be between 0 and 5.")
            return

        # Build update dict
                # Build data dict for updating
        update_data = {
            'opening_name':    name,
            'specialization':  self.spec_combo.currentText(),
            'location':        location,
            'stipend':         stipend,
            'required_gpa':    req_gpa,
            'priority':        priority,
            'deadline':        deadline_iso,
            'required_skills': skills
        }
        # Call update_opening with opening_id and data dict
        self.db.update_opening(self.opening_id, update_data)

        QMessageBox.information(self, "Saved", "Opening updated successfully.")

    def back_to_openings(self):
        """Return to the OpeningsListWindow (no save)."""
        self.next_window = OpeningsListWindow(self.user)
        self.next_window.show()
        self.close()

    def view_matches(self):
        """Open the applicants/matches view for this opening."""
        from gui.applicants_window import ApplicantsWindow
        self.next_window = ApplicantsWindow(self.opening_id)
        self.next_window.show()
        self.close()

    def view_matches(self):
        """
        Open the ApplicantsWindow for this opening by passing
        the full opening record (as a dict) instead of just its ID.
        """
        # defer import to break the circular dependency
        from gui.applicants_window import ApplicantsWindow

        # pull the full opening row from the DB
        opening_row = self.db.get_opening_by_id(self.opening_id)
        # sqlite3.Row doesn’t support .get(), so convert to dict
        try:
            opening_row = dict(opening_row)
        except Exception:
            pass

        # now hand that dict off to ApplicantsWindow
        self.next_window = ApplicantsWindow(opening_row)
        self.next_window.show()
        self.close()
