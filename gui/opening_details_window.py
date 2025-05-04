# gui/opening_details_window.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QFormLayout, QMessageBox,
    QDateTimeEdit
)
from PyQt6.QtCore import Qt, QDateTime
from database.db_manager import DBManager
from gui.openings_list_window import OpeningsListWindow

class OpeningDetailsWindow(QWidget):
    """
    Window for creating or editing a single apprenticeship opening.
    Collects specialization, location, stipend, required GPA,
    priority, deadline, and required skills, then saves to DB.
    """
    def __init__(self, company_email, opening_name):
        super().__init__()
        self.company_email = company_email
        self.opening_name = opening_name
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        """Initialize the form inputs and buttons."""
        self.setWindowTitle("Enter Apprenticeship Details")
        self.setGeometry(300, 300, 600, 350)

        form = QFormLayout()

        # 1) Specialization dropdown
        self.spec_combo = QComboBox()
        self.spec_combo.addItems([
            "Software Engineering", "Electrical Engineering", "Mechanical Engineering",
            "Civil Engineering", "Chemical Engineering", "Nuclear Engineering",
            "Industrial Engineering", "Mining Engineering"
        ])
        form.addRow(QLabel("Specialization:"), self.spec_combo)

        # 2) Location text field
        self.loc_input = QLineEdit()
        self.loc_input.setPlaceholderText("e.g., Riyadh")
        form.addRow(QLabel("Location:"), self.loc_input)

        # 3) Stipend numeric text field
        self.stip_input = QLineEdit()
        self.stip_input.setPlaceholderText("e.g., 1500")
        form.addRow(QLabel("Stipend (SAR):"), self.stip_input)

        # 4) Required GPA text field
        self.gpa_input = QLineEdit()
        self.gpa_input.setPlaceholderText("e.g., 3.5")
        form.addRow(QLabel("Required GPA (0–5):"), self.gpa_input)

        # 5) Priority dropdown (display vs stored value)
        self.priority_combo = QComboBox()
        # Display the capitalized label, store lowercase key
        self.priority_combo.addItem("Location", "location")
        self.priority_combo.addItem("GPA",      "gpa")
        form.addRow(QLabel("Priority:"), self.priority_combo)

        # 6) Deadline date/time picker (defaults to 7 days from now)
        self.deadline_edit = QDateTimeEdit()
        self.deadline_edit.setCalendarPopup(True)
        # default deadline: one week from current date/time
        self.deadline_edit.setDateTime(QDateTime.currentDateTime().addDays(7))
        form.addRow(QLabel("Deadline:"), self.deadline_edit)

        # 7) Required skills multi-line text
        self.skills_input = QTextEdit()
        self.skills_input.setPlaceholderText("List required skills, separated by commas")
        form.addRow(QLabel("Required Skills:"), self.skills_input)

        # 8) Buttons: Create Opening and Back to Openings list
        btn_create = QPushButton("Create Opening")
        btn_create.clicked.connect(self.handle_submit)
        form.addRow(btn_create)

        btn_back = QPushButton("Back to Openings")
        btn_back.clicked.connect(self.back_to_list)
        form.addRow(btn_back)

        self.setLayout(form)

    def handle_submit(self):
        """
        Validate inputs, then insert the opening record into the database.
        Finally, navigate back to the openings list.
        """
        # --- Gather raw inputs ---
        spec      = self.spec_combo.currentText()
        location  = self.loc_input.text().strip()
        stipend   = self.stip_input.text().strip()
        skills    = self.skills_input.toPlainText().strip()
        gpa_text  = self.gpa_input.text().strip()
        # priority key from combo's data
        priority  = self.priority_combo.currentData()
        # ISO‐format deadline string *with* millisecond precision,
        # so we can reliably compare & round-trip.
        dt        = self.deadline_edit.dateTime()
        deadline  = dt.toString(Qt.DateFormat.ISODateWithMs)

        # --- Field validation ---
        # All top‐level fields must be nonempty
        if not (location and stipend and gpa_text and skills):
            QMessageBox.warning(
                self, "Missing Fields", "All fields are required: location, stipend, GPA, skills."
            )
            return

        # validate stipend
        try:
            stipend_val = float(stipend)
            if stipend_val <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(
                self, "Invalid Stipend", "Stipend must be a positive number."
            )
            return

        # validate required GPA between 0 and 5
        try:
            req_gpa = float(gpa_text)
            if not (0 <= req_gpa <= 5):
                raise ValueError()
        except ValueError:
            QMessageBox.warning(
                self, "Invalid GPA", "Required GPA must be a number between 0 and 5."
            )
            return

        # --- Insert into database ---
        self.db.insert_opening({
            "company_email":   self.company_email,
            "opening_name":    self.opening_name,
            "specialization":  spec,
            "location":        location,
            "stipend":         stipend_val,
            "required_skills": skills,
            "required_gpa":    req_gpa,
            "priority":        priority,
            "deadline":        deadline
        })

        QMessageBox.information(
            self, "Success", "Your apprenticeship opening has been created!"
        )

        # --- Navigate back to openings list ---
        self.next_window = OpeningsListWindow({
            'email': self.company_email,
            'role':  'company'
        })
        self.next_window.show()
        self.close()

    def back_to_list(self):
        """Cancel creation and return to the openings list view."""
        self.next_window = OpeningsListWindow({
            'email': self.company_email,
            'role':  'company'
        })
        self.next_window.show()
        self.close()
