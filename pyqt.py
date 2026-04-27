"""import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# Create  application instance
app = QApplication(sys.argv)

# Create the main window
window = QMainWindow()
window.setWindowTitle("Simple PyQt Example")
window.setGeometry(100, 100, 400, 200)

# Create a label widget
label = QLabel("Hello, PyQt!", window)
label.move(150, 80)

# Show the window
window.show()

# Execute the application
sys.exit(app.exec())
"""
























"""import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
     ## self.initUI()  ## this is a fuction 

  ### def initUI(self):
      self.setWindowTitle("PyQt Major Classes Demo")

      # Create QLabel
      label = QLabel("Hello, PyQt!")

      # Create QPushButton
      button = QPushButton("Click Me")
      button.clicked.connect(self.onButtonClick)

      # Create a vertical layout
      layout = QVBoxLayout()
      layout.addWidget(label)
      layout.addWidget(button)

      # Create a central widget and set the layout
      central_widget = QWidget()
      central_widget.setLayout(layout)
      self.setCentralWidget(central_widget)

   def onButtonClick(self):
      print("Button clicked!")

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())"""






















"""import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def window():
   app = QApplication(sys.argv)
   win = QDialog()
   b1 = QPushButton(win)
   b1.setText("Button1")
   b1.move(50,20)
   b1.clicked.connect(b1_clicked)

   b2 = QPushButton(win)
   b2.setText("Button2")
   b2.move(50,50)
   QObject.connect(b2,SIGNAL("clicked()"),b2_clicked)

   win.setGeometry(100,100,200,100)
   win.setWindowTitle("PyQt")
   win.show()
   sys.exit(app.exec_())

def b1_clicked():
   print "Button 1 clicked"

def b2_clicked():
   print "Button 2 clicked"

if __name__ == '__main__':
   window()"""
























"""


import sys
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton
from PyQt6.QtCore import Qt

def window():
    app = QApplication(sys.argv)
    win = QDialog()
    
    # Button 1: Modern signal connection
    b1 = QPushButton(win)
    b1.setText("Button1")
    b1.move(50, 20)
    b1.clicked.connect(b1_clicked)

    # Button 2: Updated from old-style QObject.connect to modern syntax
    b2 = QPushButton(win)
    b2.setText("Button2")
    b2.move(50, 50)
    b2.clicked.connect(b2_clicked)

    win.setGeometry(100, 100, 200, 100)
    win.setWindowTitle("PyQt5")
    win.show()
    sys.exit(app.exec())

def b1_clicked():
    print("Button 1 clicked")

def b2_clicked():
    print("Button 2 clicked")

if __name__ == '__main__':
    window()
"""






















"""
import sys
from PyQt6.QtWidgets import QApplication, QPushButton

def greet():
   print("Hello, PyQt!")

def farewell():
   print("Goodbye, PyQt!")

app = QApplication(sys.argv)                                             ### baki 
button = QPushButton("Click Me")
button.clicked.connect(greet)
button.clicked.connect(farewell)
button.show()
sys.exit(app.exec())"""
















"""
from PyQt6.QtCore import QObject, pyqtSignal

class MyObject(QObject):
   # Define an unbound signal
   my_signal = pyqtSignal(int)

obj = MyObject()  # Create an instance of MyObject
obj.my_signal.connect(lambda value: print(f"Received value: {value}"))

# Emit the signal
obj.my_signal.emit(42)

print(f"Number of receivers: {obj.receivers(obj.my_signal)}") 


"""







"""
from PyQt6.QtCore import QObject, pyqtSignal


class MyObject(QObject):
   # Define a signal
   my_signal = pyqtSignal(int)

obj = MyObject()  # Create an instance of MyObject
slot = lambda value: print(f"Received value: {value}")
obj.my_signal.connect(slot)

# Emit the signal
obj.my_signal.emit(42)

# Disconnect the slot
obj.my_signal.disconnect(slot)
                                                   ## baki 
# Emit the signal again
obj.my_signal.emit(100)
print(f"Number of receivers: {obj.receivers(obj.my_signal)}") 
# Will show 1 after connect, 0 after disconnect.





"""





"""
from PyQt6.QtCore import QObject, pyqtSignal
class MyObject(QObject):
   # Define an overloaded signal
   my_signal = pyqtSignal([int], [str])

obj = MyObject()  # Create an instance of MyObject
obj.my_signal[int].connect(lambda value: print(f"Received integer value: {value}"))
obj.my_signal[str].connect(lambda value: print(f"Received string value: {value}"))

# Emit the signal with different types of arguments
obj.my_signal[int].emit(42)
obj.my_signal[str].emit("Hello PyQt")"""












"""


import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
def window():
   app = QApplication(sys.argv)
   win = QWidget()
   grid = QGridLayout()

   for i in range(1, 5):
      for j in range(1, 5):
         grid.addWidget(QPushButton("Axit"+ str(i)  ), i, j)

   win.setLayout(grid)
   win.setGeometry(100, 100, 200, 100)
   win.setWindowTitle("PyQt")
   win.show()
   sys.exit(app.exec())

if __name__ == '__main__':
   window()



"""













"""import sys
# QFileSystemModel is now in QtGui
from PyQt6.QtWidgets import QApplication, QColumnView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = QFileSystemModel()
    # Use QDir.rootPath() for a valid starting point
    model.setRootPath(QDir.rootPath())

    column_view = QColumnView()
    column_view.setModel(model)
    column_view.setWindowTitle("Fixed PyQt6 QColumnView Example")
    
    # Ensure the view shows the root directory
    column_view.setRootIndex(model.index(QDir.rootPath()))
    
    column_view.show()

    # Use .exec() instead of .exec_() in PyQt6
    sys.exit(app.exec())
"""









"""
import sys
from PyQt6.QtWidgets import QApplication, QColumnView
# In PyQt6, QFileSystemModel is located in QtGui
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = QFileSystemModel()
    # Set a valid root path to ensure columns populate correctly
    model.setRootPath(QDir.rootPath())

    column_view = QColumnView()
    column_view.setModel(model)

    # Customize column widths
    # Extra values are used for new columns as they are created
    widths = [200, 150, 250] 
    column_view.setColumnWidths(widths)

    column_view.setWindowTitle("Customized Column Widths (PyQt6)")
    
    # Optional: Set the initial view to show the root directory
    column_view.setRootIndex(model.index(QDir.rootPath()))
    
    column_view.resize(800, 400)
    column_view.show()

    # PyQt6 uses .exec() instead of .exec_()
    sys.exit(app.exec())


"""








"""


import sys
# In PyQt6, UI components are in QtWidgets
from PyQt6.QtWidgets import QApplication, QTableView
# Model and Item classes moved to QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem

# Initialize the application
app = QApplication(sys.argv)

# Create a standard item model (Now in QtGui)
model = QStandardItemModel()

# Set row and column count
model.setRowCount(4)
model.setColumnCount(3)

# Populate the model with data
for row in range(4):
   for column in range(3):
      item = QStandardItem(f'Row {row}, Column {column}')
      model.setItem(row, column, item)

# Create and configure the table view
table_view = QTableView()
table_view.setModel(model)

# Customize appearance
table_view.setWordWrap(True)
table_view.setShowGrid(False)

table_view.setWindowTitle('Customized QTableView Example (PyQt6)')
table_view.show()

# Use .exec() instead of .exec_()
sys.exit(app.exec())
"""








"""import sys
from PyQt6.QtWidgets import QApplication, QTableView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt  # Added for alignment/interaction constants

app = QApplication(sys.argv)

model = QStandardItemModel()
model.setRowCount(4)
model.setColumnCount(3)

# Adding Header Labels (Standard for TableViews)
model.setHorizontalHeaderLabels(['ID', 'Name', 'Status'])

for row in range(4):
   for column in range(3):
      item = QStandardItem(f'R{row}, C{column}')
      # Example of PyQt6 Enum usage: Center the text
      item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) 
      model.setItem(row, column, item)

table_view = QTableView()
table_view.setModel(model)

# Make the last column stretch to fit the window
header = table_view.horizontalHeader()
header.setStretchLastSection(True)

table_view.setWindowTitle('Verified PyQt6 TableView')
table_view.resize(500, 300)
table_view.show()

sys.exit(app.exec())
"""



"""from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPainter
class MyWidget(QtWidgets.QWidget):
   def paintEvent(self, event):
      painter = QtGui.QPainter(self)
      painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
      painter.setPen(QtCore.Qt.GlobalColor.green)
      painter.setBrush(QtCore.Qt.GlobalColor.white)
      painter.drawLine(50, 50, 400, 100)

app = QtWidgets.QApplication([])
widget = MyWidget()
widget.show()
app.exec()
"""







"""

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPainter, QPainterPath
class MyWidget(QtWidgets.QWidget):
   def paintEvent(self, event):
      painter = QPainter()
      path = QPainterPath()
      painter.begin(self)
      painter.setRenderHint(QPainter.RenderHint.Antialiasing)
      painter.setPen(QtCore.Qt.GlobalColor.green)
      painter.setBrush(QtCore.Qt.GlobalColor.red)
      path.moveTo(200, 200)
      path.lineTo(300, 100)
      path.lineTo(300, 200)
      path.lineTo(100, 300)
      painter.drawPath(path)
app = QtWidgets.QApplication([])
widget = MyWidget()
widget.show()
app.exec()"""




"""import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QPen
from PyQt6.QtCore import Qt

class Example(QWidget):
   def __init__(self):
      super().__init__()
      self.setGeometry(30, 30, 500, 300)
      
   def paintEvent(self, event):
      painter = QPainter(self)
      pixmap = QPixmap("C:\\Users\\axitd\\Downloads\\WhatsApp.jpeg")
      painter.drawPixmap(self.rect(), pixmap)
      
      # In PyQt6, enums must be fully qualified
      pen = QPen(Qt.GlobalColor.gray, 3)
      painter.setPen(pen)
      painter.drawRect(40, 40, 400, 200)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Example()
   ex.show()
   # .exec_() was deprecated in favor of .exec()
   sys.exit(app.exec())
"""







"""

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QGraphicsOpacityEffect, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

# Set the path
image_path = r"C:\Users\axitd\OneDrive\Pictures\1132043.jpg"
image_label = QLabel()
image_pixmap = QPixmap(image_path)
image_label.setPixmap(image_pixmap)

# Create a QGraphicsOpacityEffect
opacity_effect = QGraphicsOpacityEffect()
# Setting Opacity
opacity_effect.setOpacity(0.5)  
image_label.setGraphicsEffect(opacity_effect)

layout.addWidget(image_label)
window.setLayout(layout)
window.show()

sys.exit(app.exec())



"""


