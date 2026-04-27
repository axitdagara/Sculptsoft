import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem,
    QStackedWidget, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

# ------------------ DATABASE ------------------
def create_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("student_professional.db")
    if not db.open():
        print("Database connection failed")
        return

    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    # Insert default admin
    query.exec("SELECT * FROM users")
    if not query.next():
        query.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
        query.addBindValue("admin")
        query.addBindValue("admin")
        query.exec()

    # Students Table
    query.exec("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    """)

# ------------------ MAIN APPLICATION ------------------
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Student Management System")
        self.setGeometry(150, 100, 700, 500)
        self.is_dark = False

        # ------------------ STACKED WIDGET ------------------
        self.stack = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        # ------------------ SCREENS ------------------
        self.login_screen()
        self.dashboard_screen()
        self.student_screen()

        self.stack.setCurrentWidget(self.login_widget)
        self.apply_light_theme()

    
    def login_screen(self):
        self.login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(200, 100, 200, 100)

        title = QLabel("Login")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.check_login)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(login_btn)

        self.login_widget.setLayout(layout)
        self.stack.addWidget(self.login_widget)

    def check_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(username)
        query.addBindValue(password)
        query.exec()
        if query.next():
            self.stack.setCurrentWidget(self.dashboard_widget)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

   
    def dashboard_screen(self):
        self.dashboard_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Dashboard")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        theme_btn = QPushButton("Toggle Light/Dark Mode")
        theme_btn.clicked.connect(self.toggle_theme)

        student_btn = QPushButton("Student Management System")
        student_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.student_widget))

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(theme_btn)
        layout.addWidget(student_btn)

        self.dashboard_widget.setLayout(layout)
        self.stack.addWidget(self.dashboard_widget)

    # ------------------ STUDENT SCREEN ------------------
    def student_screen(self):
        self.student_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)

        title = QLabel("Student Management System")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Inputs
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")
        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Course")
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.age_input)
        input_layout.addWidget(self.course_input)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        update_btn = QPushButton("Update")
        delete_btn = QPushButton("Delete")
        back_btn = QPushButton("Back")
        add_btn.clicked.connect(self.add_student)
        update_btn.clicked.connect(self.update_student)
        delete_btn.clicked.connect(self.delete_student)
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_widget))
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(back_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Course"])
        self.table.cellClicked.connect(self.load_selected_student)

        layout.addWidget(title)
        layout.addLayout(input_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)

        self.student_widget.setLayout(layout)
        self.stack.addWidget(self.student_widget)

        self.load_students()

    # ------------------ STUDENT METHODS ------------------
    def load_students(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM students")
        row = 0
        while query.next():
            self.table.insertRow(row)
            for col in range(4):
                self.table.setItem(row, col, QTableWidgetItem(str(query.value(col))))
            row += 1

    def load_selected_student(self, row, col):
        self.name_input.setText(self.table.item(row,1).text())
        self.age_input.setText(self.table.item(row,2).text())
        self.course_input.setText(self.table.item(row,3).text())

    def add_student(self):
        name = self.name_input.text()
        age = self.age_input.text()
        course = self.course_input.text()
        query = QSqlQuery()
        query.prepare("INSERT INTO students (name, age, course) VALUES (?, ?, ?)")
        query.addBindValue(name)
        query.addBindValue(age)
        query.addBindValue(course)
        query.exec()
        self.load_students()

    def update_student(self):
        row = self.table.currentRow()
        if row < 0: return
        student_id = self.table.item(row,0).text()
        query = QSqlQuery()
        query.prepare("UPDATE students SET name=?, age=?, course=? WHERE id=?")
        query.addBindValue(self.name_input.text())
        query.addBindValue(self.age_input.text())
        query.addBindValue(self.course_input.text())
        query.addBindValue(student_id)
        query.exec()
        self.load_students()

    def delete_student(self):
        row = self.table.currentRow()
        if row < 0: return
        student_id = self.table.item(row,0).text()
        query = QSqlQuery()
        query.prepare("DELETE FROM students WHERE id=?")
        query.addBindValue(student_id)
        query.exec()
        self.load_students()

    # ------------------ THEME ------------------
    def toggle_theme(self):
        if self.is_dark:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
        self.is_dark = not self.is_dark

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #f0f0f0; color: #000; font-size: 14px; }
            QPushButton { background-color: #0078d7; color: white; padding: 6px 12px; border-radius: 5px; }
            QPushButton:hover { background-color: #005ea6; }
            QLineEdit { padding: 5px; border-radius: 5px; border: 1px solid #ccc; }
            QTableWidget { background-color: #fff; gridline-color: #ccc; }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #2c2c2c; color: #fff; font-size: 14px; }
            QPushButton { background-color: #444; color: #fff; padding: 6px 12px; border-radius: 5px; }
            QPushButton:hover { background-color: #555; }
            QLineEdit { padding: 5px; border-radius: 5px; border: 1px solid #555; background-color: #333; color: #fff; }
            QTableWidget { background-color: #3c3c3c; gridline-color: #555; color: #fff; }
        """)

# ------------------ MAIN ------------------
app = QApplication(sys.argv)
create_database()
window = MainApp()
window.show()
sys.exit(app.exec())