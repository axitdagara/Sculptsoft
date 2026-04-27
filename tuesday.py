"""import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class DirectoryOpenExample(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Directory Selection Example")
      self.setGeometry(300, 200, 400, 200)

      button = QPushButton("Open Directory", self)
      button.setGeometry(150, 80, 100, 30)
      button.clicked.connect(self.open_directory)

   def open_directory(self):
      directory = QFileDialog.getExistingDirectory(self, "Open Directory", "")
      if directory:
         print("Selected Directory:", directory)

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = DirectoryOpenExample()
   window.show()
   sys.exit(app.exec())"""













"""import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()

      self.setWindowTitle("Toggleable Action Example")

      self.toggle_action = QAction("Toggle", self, checkable=True)
      self.toggle_action.triggered.connect(self.display_message)

      self.addAction(self.toggle_action)

      self.toggle_button = QPushButton("Toggle Action", self)
      self.toggle_button.clicked.connect(self.toggle_action.trigger)

   def display_message(self, checked):
      if checked:
         QMessageBox.information(self, "Message", "Action Checked!")
      else:
         QMessageBox.information(self, "Message", "Action Unchecked!")

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())"""














"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer


class ToggleWidget(QWidget):
   def __init__(self):
      super().__init__()
      self.initUI()

   def initUI(self):
      self.button = QPushButton("Toggle Widget")
      self.button.clicked.connect(self.toggle_visibility)
      layout = QVBoxLayout()
      layout.addWidget(self.button)
      self.setLayout(layout)

   def hideEvent(self, event):
      print("Widget is now hidden")

   def toggle_visibility(self):
      self.setVisible(not self.isVisible())
      if not self.isVisible():
         QTimer.singleShot(2000, self.show)
def main():
   app = QApplication(sys.argv)
   widget = ToggleWidget()
   widget.show()
   sys.exit(app.exec())

if __name__ == "__main__":
   main()"""

















"""

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QSize

class CustomWidget(QWidget):
   def __init__(self):
      super().__init__()

   def resizeEvent(self, event):
      print("Widget resized to:", event.size())

if __name__ == '__main__':
   app = QApplication([])
   widget = CustomWidget()
   widget.resize(700, 200)
   widget.show()
   app.exec()"""










"""

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class DynamicWidget(QWidget):
   def __init__(self):
      super().__init__()
      self.label = QLabel("Resize me!")
      layout = QVBoxLayout(self)
      layout.addWidget(self.label)

   def resizeEvent(self, event):
      if event.size().width() < 200:
         self.label.setText("Too small!")
      else:
         self.label.setText("Resize me!")

if __name__ == '__main__':
   app = QApplication([])
   widget = DynamicWidget()
   widget.resize(60, 20)
   widget.show()
   app.exec()"""
















import sys
from PyQt6.QtWidgets import (QApplication, QTableView, QVBoxLayout, 
                             QPushButton, QDialog, QMessageBox)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt

def initializeModel(model):
    model.setTable('sportsmen')
    # Strategy: OnFieldChange applies edits immediately to the DB
    model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
    model.select()
    # Updated headers using PyQt6 Enum paths
    model.setHeaderData(0, Qt.Orientation.Horizontal, "ID")
    model.setHeaderData(1, Qt.Orientation.Horizontal, "First Name")
    model.setHeaderData(2, Qt.Orientation.Horizontal, "Last Name")

def add_row(model):
    # insertRow returns True if successful
    if not model.insertRow(model.rowCount()):
        print("Failed to insert row")

def delete_row(view, model):
    index = view.currentIndex()
    if index.isValid():
        model.removeRow(index.row())
        model.select() # Refresh the view
    else:
        QMessageBox.warning(None, "Selection Error", "Please select a row to delete.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 1. Setup Database Connection
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('sports.db')
    if not db.open():
        QMessageBox.critical(None, "Error", "Could not open database")
        sys.exit(1)

    # 2. Setup Model and View
    model = QSqlTableModel()
    initializeModel(model)

    view = QTableView()
    view.setModel(model)

    # 3. UI Layout
    dlg = QDialog()
    dlg.setWindowTitle("PyQt6 Database Demo")
    layout = QVBoxLayout(dlg)
    layout.addWidget(view)

    btn_add = QPushButton("Add Sportsperson")
    btn_add.clicked.connect(lambda: add_row(model))
    layout.addWidget(btn_add)

    btn_del = QPushButton("Delete Selected")
    btn_del.clicked.connect(lambda: delete_row(view, model))
    layout.addWidget(btn_del)

    dlg.resize(400, 300)
    dlg.show()
    sys.exit(app.exec())





















