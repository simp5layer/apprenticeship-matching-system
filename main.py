# main.py

import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow
from gui.student_dashboard import StudentDashboard
from gui.company_dashboard import CompanyDashboard
from gui.admin_dashboard import AdminDashboard

def main():
    app = QApplication(sys.argv)

    # If you pass an extra arg, use test‐mode:
    #   python main.py student
    #   python main.py company
    #   python main.py admin
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "student":
            dummy = {
                "name": "Test Student",
                "student_id": "S000",
                "specialization": "Electronics",
                "gpa": 4.0,
                "preferred_locations": ["CityA", "CityB", "CityC"]
            }
            window = StudentDashboard(dummy)
        elif mode == "company":
            dummy = {"name": "TestCo", "company_id": 123}
            window = CompanyDashboard(dummy)
        elif mode == "admin":
            window = AdminDashboard()
        else:
            print(f"Unknown mode '{mode}', falling back to login.")
            window = LoginWindow()
    else:
        # Default: normal login flow
        window = LoginWindow()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
