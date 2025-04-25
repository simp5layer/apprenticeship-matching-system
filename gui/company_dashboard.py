from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
)
from database.db_manager import DBManager

class CompanyDashboard(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Company Dashboard — {self.user['name']}")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Welcome, {self.user['name']}!"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Specialization", "Location", "Stipend"])
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        btn_add = QPushButton("Add Opening")
        btn_edit = QPushButton("Edit Selected")
        btn_delete = QPushButton("Delete Selected")
        btn_add.clicked.connect(self.add_opening)
        btn_edit.clicked.connect(self.edit_opening)
        btn_delete.clicked.connect(self.delete_opening)

        layout.addWidget(btn_add)
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        self.setLayout(layout)
        self.load_openings()

    def load_openings(self):
        openings = self.db.get_openings_by_company(self.user["company_id"])
        self.table.setRowCount(len(openings))
        for i, op in enumerate(openings):
            self.table.setItem(i, 0, QTableWidgetItem(str(op["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(op["specialization"]))
            self.table.setItem(i, 2, QTableWidgetItem(op["location"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(op["stipend"])))

    def add_opening(self):
        pass

    def edit_opening(self):
        pass

    def delete_opening(self):
        pass
