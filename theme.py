import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout
)


class ThemeSwitcher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Theme Switcher App")
        self.setGeometry(200, 200, 400, 250)

        self.is_dark = False  

       
        self.label = QLabel(" Theme Switcher ")

          
        self.label.setStyleSheet("font-size: 18px; text-align: center;")
        self.label.setAlignment(self.label.alignment() | 0x0004)            ## online

        self.button = QPushButton("change Theme")
        self.button.clicked.connect(self.toggle_theme)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.apply_light_theme()  # Start with light theme

    def toggle_theme(self):
        if self.is_dark:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()

        self.is_dark = not self.is_dark

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QPushButton {
                background-color: #e0e0e0;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: Pink;
            }"""
        )

    def apply_dark_theme(self):
        self.setStyleSheet ("""
            QWidget {
                background-color: #2c2c2c;
                color: white;
            }
            QPushButton {
                background-color: #444;
                padding: 8px;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: black;
            }"""
        )


app = QApplication(sys.argv)
window = ThemeSwitcher()
window.show()
sys.exit(app.exec())