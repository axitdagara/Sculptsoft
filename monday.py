import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtCore import Qt

class CustomWidget(QWidget):
   def mousePressEvent(self, event):
      if event.button() == Qt.MouseButton.LeftButton:
         QMessageBox.information(self, 'Mouse Click', f'Clicked at: {event.pos()}')

app = QApplication(sys.argv)
widget = CustomWidget()
widget.show()
sys.exit(app.exec())





