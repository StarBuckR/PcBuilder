import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymongo
import pyqtgraph as pg 
import os

sys.path.insert(1, os.getcwd() + '/src/helpers/')
sys.path.insert(1, os.getcwd() + '/src/scripts/')

if not os.path.exists("./fonts/OFL.txt"):
    import download_file as df
    df.download_fonts()

from builder import builder
from graph import Graph

class Main(QWidget):
    # Main Page
    def __init__(self):
        super(QWidget, self).__init__()
        QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")
        #creating main page
        self.title = 'Graph'
        self.left = 0
        self.top = 0
        self.width = 700
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet(
            "background-color:rgb(37,35,35);"
            "font-family:Quantico;"
            "color:black;")

        # Initialize Combobox Screen
        self.layout = QVBoxLayout()     
        self.box1 = QPushButton
        self.layout.addWidget(self.box1)

        self.setLayout(self.layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Graph(700)
    sys.exit(app.exec_())
