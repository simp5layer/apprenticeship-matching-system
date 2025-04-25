import pytest
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow
from gui.student_dashboard import StudentDashboard
from gui.company_dashboard import CompanyDashboard
from gui.admin_dashboard import AdminDashboard

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance() or QApplication([])
    return app

def test_login_window_components(app, qtbot):
    win = LoginWindow()
    qtbot.addWidget(win)
    assert win.email is not None
    assert win.password is not None
    assert win.login_btn.text() == 'Login'
    assert win.register_btn.text() == 'Register'

def test_student_dashboard(app, qtbot):
    dummy_user = {
        "name": "Test Student",
        "student_id": "S001",
        "specialization": "Electronics",
        "gpa": 4.0,
        "preferred_locations": ["CityA", "CityB", "CityC"]
    }
    win = StudentDashboard(dummy_user)
    qtbot.addWidget(win)
    assert hasattr(win, "show_matches")
    assert "Student Dashboard" in win.windowTitle()

def test_company_dashboard(app, qtbot):
    dummy_user = {"name": "TestCo", "company_id": 1}
    win = CompanyDashboard(dummy_user)
    qtbot.addWidget(win)
    assert win.table.columnCount() == 4
    assert "Company Dashboard" in win.windowTitle()

def test_admin_dashboard(app, qtbot):
    win = AdminDashboard()
    qtbot.addWidget(win)
    assert win.user_table.columnCount() == 3
    assert win.windowTitle() == "Admin Dashboard"
