import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout,
    QGridLayout
)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Calculator")
        self.setGeometry(200, 200, 300, 200)

        
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Enter first number")

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Enter second number")

        
        self.result_label = QLabel("Result: ")
        
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
        num1, num2 = self.get_values()
        if num1 is not None:
            self.result_label.setText(f"Result: {num1 + num2}")

    def subtract(self):
        num1, num2 = self.get_values()
        if num1 is not None:
            self.result_label.setText(f"Result: {num1 - num2}")

    def multiply(self):
        num1, num2 = self.get_values()
        if num1 is not None:
            self.result_label.setText(f"Result: {num1 * num2}")

    def divide(self):
        num1, num2 = self.get_values()
        if num1 is not None:
            if num2 == 0:
                self.result_label.setText("Cannot divide by zero!")
            else:
                self.result_label.setText(f"Result: {num1 / num2}")


app = QApplication(sys.argv)
window = Calculator()
window.show()
sys.exit(app.exec())