import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

# ------------------ DATABASE ------------------
def create_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("app_all_in_one.db")
    if not db.open():
        print("Database connection failed")
        return

    query = QSqlQuery()
    # Users table
    query.exec("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    # Insert dummy user if not exists
    query.exec("SELECT * FROM users")
    if not query.next():
        query.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
        query.addBindValue("admin")
        query.addBindValue("admin")
        query.exec()

    # Students table
    query.exec("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    """)

# ------------------ LOGIN WINDOW ------------------
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 200, 300, 150)

        self.user_label = QLabel("Username:")
        self.user_input = QLineEdit()
        self.pass_label = QLabel("Password:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)

        layout = QVBoxLayout()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def check_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(username)
        query.addBindValue(password)
        query.exec()
        if query.next():
            self.dashboard = DashboardWindow()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

# ------------------ DASHBOARD WINDOW ------------------
class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard - All-in-One App")
        self.setGeometry(200, 100, 600, 400)
        self.is_dark = False

        # Buttons
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.calc_btn = QPushButton("Open Calculator")
        self.calc_btn.clicked.connect(self.open_calculator)
        self.student_btn = QPushButton("Open Student System")
        self.student_btn.clicked.connect(self.open_student_system)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to All-in-One PyQt6 App"))
        layout.addWidget(self.theme_btn)
        layout.addWidget(self.calc_btn)
        layout.addWidget(self.student_btn)
        self.setLayout(layout)

        self.apply_light_theme()

    # ------------------ THEME ------------------
    def toggle_theme(self):
        if self.is_dark:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
        self.is_dark = not self.is_dark

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: white; color: black; }
            QPushButton { background-color: #e0e0e0; padding: 8px; border-radius: 5px; }
            QPushButton:hover { background-color: #cfcfcf; }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #2c2c2c; color: white; }
            QPushButton { background-color: #444; padding: 8px; border-radius: 5px; color: white; }
            QPushButton:hover { background-color: #555; }
        """)

    # ------------------ CALCULATOR ------------------
    def open_calculator(self):
        self.calc_window = CalculatorWindow()
        self.calc_window.show()

    # ------------------ STUDENT SYSTEM ------------------
    def open_student_system(self):
        self.student_window = StudentWindow()
        self.student_window.show()

# ------------------ CALCULATOR WINDOW ------------------
class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(250, 150, 300, 200)

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Enter first number")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Enter second number")
        self.result_label = QLabel("Result:")

        self.btn_add = QPushButton("Add")
        self.btn_sub = QPushButton("Subtract")
        self.btn_mul = QPushButton("Multiply")
        self.btn_div = QPushButton("Divide")

        self.btn_add.clicked.connect(self.add)
        self.btn_sub.clicked.connect(self.subtract)
        self.btn_mul.clicked.connect(self.multiply)
        self.btn_div.clicked.connect(self.divide)

        layout = QVBoxLayout()
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)

        grid = QGridLayout()
        grid.addWidget(self.btn_add, 0, 0)
        grid.addWidget(self.btn_sub, 0, 1)
        grid.addWidget(self.btn_mul, 1, 0)
        grid.addWidget(self.btn_div, 1, 1)

        layout.addLayout(grid)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def get_values(self):
        try:
            num1 = float(self.input1.text())
            num2 = float(self.input2.text())
            return num1, num2
        except ValueError:
            self.result_label.setText("Invalid input!")
            return None, None

    def add(self):
        n1, n2 = self.get_values()
        if n1 is not None: self.result_label.setText(f"Result: {n1+n2}")

    def subtract(self):
        n1, n2 = self.get_values()
        if n1 is not None: self.result_label.setText(f"Result: {n1-n2}")

    def multiply(self):
        n1, n2 = self.get_values()
        if n1 is not None: self.result_label.setText(f"Result: {n1*n2}")

    def divide(self):
        n1, n2 = self.get_values()
        if n1 is not None:
            if n2 == 0:
                self.result_label.setText("Cannot divide by zero!")
            else:
                self.result_label.setText(f"Result: {n1/n2}")

# ------------------ STUDENT WINDOW ------------------
class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(200, 150, 600, 400)

        # Inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")
        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Course")

        # Buttons
        self.btn_add = QPushButton("Add")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_add.clicked.connect(self.add_student)
        self.btn_update.clicked.connect(self.update_student)
        self.btn_delete.clicked.connect(self.delete_student)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Course"])
        self.table.cellClicked.connect(self.load_selected)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_input)
        layout.addWidget(self.course_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data()

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
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM students")
        row = 0
        while query.next():
            self.table.insertRow(row)
            for col in range(4):
                self.table.setItem(row, col, QTableWidgetItem(str(query.value(col))))
            row += 1

    def load_selected(self, row, column):
        self.name_input.setText(self.table.item(row,1).text())
        self.age_input.setText(self.table.item(row,2).text())
        self.course_input.setText(self.table.item(row,3).text())

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
        self.load_data()

    def delete_student(self):
        row = self.table.currentRow()
        if row < 0: return
        student_id = self.table.item(row,0).text()
        query = QSqlQuery()
        query.prepare("DELETE FROM students WHERE id=?")
        query.addBindValue(student_id)
        query.exec()
        self.load_data()

# ------------------ MAIN ------------------
app = QApplication(sys.argv)
create_database()
login = LoginWindow()
login.show()
sys.exit(app.exec())