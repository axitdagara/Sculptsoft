from PyQt6 import QtWidgets, uic
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self) # Dynamically loads PyQt6 UI
        self.pushButton.clicked.connect(self.clickhandler)
        self.pushButton_2.clicked.connect(self.clickhandler2)
    def clickhandler(self):
        print("hello")
    def clickhandler2(self):
       print("hellooo")    


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()
