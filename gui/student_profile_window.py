# gui/student_profile_window.py

from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager

class StudentProfileWindow(QWidget):
    def __init__(self, email: str):
        super().__init__()
        self.email = email
        self.db = DBManager()
        self.existing = self.db.get_student_by_email(email) is not None
        self.init_ui()

    def init_ui(self):
        title = "Edit Your Student Profile" if self.existing else "Create Your Student Profile"
        self.setWindowTitle(title)
        self.setGeometry(300, 300, 500, 500)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_in = QLineEdit()
        form.addRow(QLabel("Name:"), self.name_in)

        self.mobile_in = QLineEdit()
        form.addRow(QLabel("Mobile Number:"), self.mobile_in)

        self.id_in = QLineEdit()
        form.addRow(QLabel("Student ID:"), self.id_in)

        self.gpa_in = QLineEdit()
        self.gpa_in.setPlaceholderText("0.0 - 5.0")
        form.addRow(QLabel("GPA (0–5):"), self.gpa_in)

        self.spec_combo = QComboBox()
        self.spec_combo.addItems([
            "Software Engineering","Electrical Engineering","Mechanical Engineering",
            "Civil Engineering","Chemical Engineering","Nuclear Engineering",
            "Industrial Engineering","Mining Engineering"
        ])
        form.addRow(QLabel("Specialization:"), self.spec_combo)

        self.pref1 = QLineEdit()
        self.pref2 = QLineEdit()
        self.pref3 = QLineEdit()
        form.addRow(QLabel("Preferred Location 1:"), self.pref1)
        form.addRow(QLabel("Preferred Location 2:"), self.pref2)
        form.addRow(QLabel("Preferred Location 3:"), self.pref3)

        self.skills_in = QTextEdit()
        form.addRow(QLabel("Skills (comma-separated):"), self.skills_in)

        btn_text = "Update Profile" if self.existing else "Save Profile"
        self.submit_btn = QPushButton(btn_text)
        self.submit_btn.clicked.connect(self.handle_submit)
        form.addRow(self.submit_btn)

        self.setLayout(form)

        if self.existing:
            row = self.db.get_student_by_email(self.email)
            self.id_in.setText(row['student_id'])
            self.name_in.setText(row['name'])
            self.mobile_in.setText(row['mobile_number'])
            self.gpa_in.setText(str(row['gpa']))
            idx = self.spec_combo.findText(row['specialization'])
            if idx >= 0:
                self.spec_combo.setCurrentIndex(idx)
            prefs = row['preferred_locations'].split(';') if row['preferred_locations'] else []
            for i, pref in enumerate(prefs[:3]):
                getattr(self, f'pref{i+1}').setText(pref)
            self.skills_in.setPlainText(row['skills'])

    def handle_submit(self):
        try:
            gpa_val = float(self.gpa_in.text().strip())
            assert 0 <= gpa_val <= 5
        except:
            QMessageBox.warning(self, "Invalid GPA", "GPA must be between 0 and 5.")
            return

        prefs = [f.text().strip() for f in (self.pref1, self.pref2, self.pref3) if f.text().strip()]
        if not prefs:
            QMessageBox.warning(self, "Missing Location", "Please enter at least one preferred location.")
            return

        data = {
            'student_id':         self.id_in.text().strip(),
            'name':               self.name_in.text().strip(),
            'mobile_number':      self.mobile_in.text().strip(),
            'email':              self.email,
            'gpa':                gpa_val,
            'specialization':     self.spec_combo.currentText(),
            'preferred_locations':';'.join(prefs),
            'skills':             self.skills_in.toPlainText().strip()
        }

        # check required fields
        for key in ('student_id','name','mobile_number','skills'):
            if not data[key]:
                QMessageBox.warning(self, "Missing Fields", f"{key.replace('_',' ').title()} is required.")
                return

        try:
            if self.existing:
                self.db.update_student(self.email, data)
                QMessageBox.information(self, "Success", "Profile updated successfully.")
            else:
                # check duplicate student ID
                if self.db.get_student_by_id(data['student_id']):
                    QMessageBox.warning(self, "Duplicate ID", "That Student ID already exists.")
                    return
                self.db.insert_student(data)
                QMessageBox.information(self, "Success", "Profile created successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unable to save profile: {e}")
            return

        # Go to student dashboard
        from gui.student_dashboard import StudentDashboard
        self.next_window = StudentDashboard(self.db.get_student_by_email(self.email))
        self.next_window.show()
        self.close()
