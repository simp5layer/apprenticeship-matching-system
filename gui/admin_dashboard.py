from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from database.db_manager import DBManager

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Admin Dashboard")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("User Management"))

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Email", "Name", "Role"])
        self.user_table.setSortingEnabled(True)
        layout.addWidget(self.user_table)

        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.load_users)
        layout.addWidget(btn_refresh)

        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        users = self.db.get_all_users()
        self.user_table.setRowCount(len(users))
        for i, u in enumerate(users):
            self.user_table.setItem(i, 0, QTableWidgetItem(u["email"]))
            self.user_table.setItem(i, 1, QTableWidgetItem(u["name"]))
            self.user_table.setItem(i, 2, QTableWidgetItem(u["role"]))
