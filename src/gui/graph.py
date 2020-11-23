import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymongo
import pyqtgraph as pg 
import os

if not os.path.exists("./fonts/OFL.txt"):
    import download_file as df
    df.download_fonts()

class App(QWidget):
    # Main Page
    def __init__(self,):
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
        self.box1 = QComboBox()
        self.box2 = QComboBox()

        self.names = ["MOTHERBOARD","RAM","GPU","CPU","SSD","HDD"]
        self.box1.currentTextChanged.connect(self.updateSecondBox)
        self.box1.addItems(self.names)

        self.layout.addWidget(self.box1)
        self.layout.addWidget(self.box2)

        self.graph = self.createBarGraph("MOTHERBOARD","Rank","Price", 20) 
        self.layout.addWidget(self.graph)

        self.setLayout(self.layout)
        self.show()

    def updateSecondBox(self,text):
        self.box2.clear()
        if text == "MOTHERBOARD":
            self.box2.addItems(("Rank", "Price" , "Memory Max", "MHZ"))
        elif text == "RAM":
            self.box2.addItems(("Rank", "Price", "MHZ", "Total Memory", "CL"))
        elif text == "GPU":
            self.box2.addItems(("Rank", "Price","Gameplay Benchmark","Desktop Benchmark","Workstation Benchmark"))
        elif text == "CPU":
            self.box2.addItems(("Rank", "Price","Gameplay Benchmark","Desktop Benchmark","Workstation Benchmark"))
        elif text == "SSD":
            self.box2.addItems(("Rank", "Price", "Storage"))
        elif text == "HDD":
            self.box2.addItems(("Rank", "Price", "Storage"))
        self.database = text
        self.box2.currentTextChanged.connect(self.pullBarGraph)

    def pullBarGraph(self,text):
        self.sortindex = text
        self.layout.removeWidget(self.graph)
        self.graph = self.createBarGraph(self.database,self.sortindex,"Price-Performance", 20)  
        self.layout.addWidget(self.graph)


    # Creating a Bar Graph 
    def createBarGraph(self,database, sortindex, finderindex, number , name = None, brand = None):

        pg.setConfigOption('background', (37,35,35))
        plot = pg.PlotWidget()
        
        bandict = ["URL","Url","Rank","Benchmark","Price-Performance","_id","Latency","Ram Count"]
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["PcBuilder"]
        mycol = mydb[database]
        values = mycol.find({}, sort=[(sortindex,-1)]).limit(number)
        a=0 #for changing colors
        b=1 #counter

        color = ['b','y','g','r','d','w','c','k']

        label_style = {'color': '#EEE', 'font-size': '14pt'}
        lbl1 = sortindex
        plot.setLabel("left", lbl1, **label_style)  
        plot.setLabel("bottom", "Sıralama",**label_style)
    
        for value in values:
            y = int(value[sortindex])   
            bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush=color[a])
            plot.addItem(bg)         

            tooltip = ""
            for key in value:
                if not key in bandict:
                    tooltip += key + ": " + str(value[key]) + "\n"
            bg.setToolTip(tooltip.strip())
            plot.addItem(bg)  

            if database != "MOTHERBOARD":
                text = pg.TextItem(text=value["Brand"]+value["Model"] , color=(200, 200, 200),angle=0)
                text.setPos(b,y*1.05)
                plot.addItem(text)
            else:
                text = pg.TextItem(text=value["Brand"], color=(200, 200, 200), angle=0)
                text.setPos(b,y*1.05)
                plot.addItem(text)

            a += 1
            b += 1
            if a == 6:
                a = 0
        plot.setLimits(xMin = 0, xMax= b*1.1,yMin=-15)
        return plot
        
    # Changes Graph In The Tab    
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
