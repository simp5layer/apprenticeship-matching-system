# gui/openings_list_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QListView,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from database.db_manager import DBManager
from gui.entry_window import EntryWindow

class OpeningsListWindow(QWidget):
    def __init__(self, user_row):
        super().__init__()
        self.user = user_row               # expects dict/Row with ['email']
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"My Apprenticeship Openings – {self.user['email']}")
        self.setGeometry(250, 250, 600, 450)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Your Created Openings:")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListView.ViewMode.IconMode)
        layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        self.logout_btn = QPushButton("Log Out")
        self.logout_btn.clicked.connect(self.log_out)
        btn_layout.addWidget(self.logout_btn)

        self.issue_btn = QPushButton("Issue New Opening")
        self.issue_btn.clicked.connect(self.issue_new)
        btn_layout.addWidget(self.issue_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Populate list
        self.load_openings()

    def load_openings(self):
        """
        Refresh the list with each opening displayed alongside a Delete button.
        """
        self.list_widget.clear()
        openings = self.db.get_openings_by_company(self.user['email'])
        for o in openings:
            # Create a container widget
            container = QWidget()
            hbox = QHBoxLayout()
            hbox.setContentsMargins(5, 2, 5, 2)

            # Opening label
            label = QLabel(f"[{o['opening_id']}] {o['opening_name']}")
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            hbox.addWidget(label, stretch=1)

            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, oid=o['opening_id']: self.edit_opening(oid))
            hbox.addWidget(edit_btn)

            # Delete button
            del_btn = QPushButton("Delete")
            del_btn.clicked.connect(lambda _, oid=o['opening_id'], name=o['opening_name']: self.confirm_delete(oid, name))
            hbox.addWidget(del_btn)

            container.setLayout(hbox)

            # Insert into list
            item = QListWidgetItem()
            item.setSizeHint(container.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, container)

    def log_out(self):
        # Keep a reference so it isn't garbage-collected
        self.next_window = EntryWindow()
        self.next_window.show()
        self.close()


    def issue_new(self):
        from gui.opening_name_window import OpeningNameWindow
        self.next_window = OpeningNameWindow(self.user['email'])
        self.next_window.show()
        self.close()

    def edit_opening(self, opening_id):
        # defer the import until runtime to avoid circularity
        from gui.company_dashboard import CompanyDashboard
        self.next_window = CompanyDashboard(self.user, opening_id)
        self.next_window.show()
        self.close()

    def confirm_delete(self, opening_id, opening_name):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{opening_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_opening(opening_id)
            QMessageBox.information(self, "Deleted", f"Deleted opening '{opening_name}'.")
            self.load_openings()
