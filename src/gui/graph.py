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

class App(QWidget):
    # Main Page
    def __init__(self,Money):
        super(QWidget, self).__init__()
        QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")
        self.pullBuilder(Money)
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
        self.box2.currentTextChanged.connect(self.pullBarGraph)

        self.bandict = ["URL","Url","Benchmark","_id","Ram Count","Total Price","Please Choose Part","Brand","Model","Socket","Chipset OC","Chipset","Gb","Atx"]
        self.names = ["Please Choose Part","MOTHERBOARD","RAM","GPU","CPU","SSD","HDD"]
        self.box1.addItems(self.names)
        self.box1.currentTextChanged.connect(self.updateSecondBox)

        self.layout.addWidget(self.box1)
        self.layout.addWidget(self.box2)

        pg.setConfigOption('background', (37,35,35))
        self.graph = pg.PlotWidget()
        self.layout.addWidget(self.graph)

        self.setLayout(self.layout)
        self.show()

    def pullBuilder(self,Amount):
        self.pcs = builder(Amount,None)

        self.motherboardId = self.pcs[0]["Motherboard"]["_id"]
        self.ramId = self.pcs[0]["RAM"]["_id"]
        self.gpuId = self.pcs[0]["GPU"]["_id"]
        self.cpuId = self.pcs[0]["CPU"]["_id"]
        self.ssdId = self.pcs[0]["SSD"]["_id"]
        self.hddId = self.pcs[0]["HDD"]["_id"]

    def updateSecondBox(self):
        self.database = self.box1.currentText()
        text = self.box1.currentText()
        self.box2.clear()
        self.box2.setEnabled(False)

        values = self.pcs
        """print(values)"""
        tooltip = ""

        for value in values:
            if text =="MOTHERBOARD":
                text = "Motherboard"
            print(text)
            if not value[text] in self.bandict:
                for keys in value[text]:
                    if not keys in self.bandict:
                        self.box2.addItem(keys)
                        self.box2.setEnabled(True)
  
    def pullBarGraph(self,text):
        self.sortindex = text

        if self.sortindex == "":
            pass
        else:
            self.layout.removeWidget(self.graph)

        if self.database == "MOTHERBOARD":
            self.graph = self.createBarGraph(self.database,self.sortindex,self.motherboardId, 30)
        elif self.database == "RAM":
            self.graph = self.createBarGraph(self.database,self.sortindex,self.ramId, 30)
        elif self.database == "GPU":
            self.graph = self.createBarGraph(self.database,self.sortindex,self.gpuId, 30)
        elif self.database == "CPU":
            self.graph = self.createBarGraph(self.database,self.sortindex,self.cpuId, 30)
        elif self.database == "SSD":
            self.graph = self.createBarGraph(self.database,self.sortindex,self.ssdId, 30)
        elif self.database == "HDD":
            self.graph = self.createBarGraph(self.database,self.sortindex,self.hddId, 30)

        self.layout.addWidget(self.graph)

    # Creating a Bar Graph 
    def createBarGraph(self,database, sortindex, finderindex, number):

        plot = pg.PlotWidget()
        
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["PcBuilder"]
        mycol = mydb[database]

        findervalue = mycol.find({"_id": finderindex})
        if int(findervalue[0]["Rank"]) < 20:
            itemrank = int(findervalue[0]["Rank"])
            skipvalue =int(itemrank)
            values = mycol.find({}, sort=[("Rank",1)]).limit(number)

        elif int(findervalue[0]["Rank"])>=20 and int(findervalue[0]["Rank"]) < 60:
            itemrank = int(findervalue[0]["Rank"])
            skipvalue =int(itemrank-(number/2))
            values = mycol.find({}, sort=[("Rank",1)]).limit(number).skip(skipvalue)

        elif int(findervalue[0]["Rank"])>=60:
            itemrank = int(findervalue[0]["Rank"])
            skipvalue = int(itemrank-(number))
            values = mycol.find({}, sort=[("Rank",1)]).limit(number).skip(skipvalue)

        a=0 #for changing colors
        b=1 #counter

        color = ['y','w','c']

        label_style = {'color': '#EEE', 'font-size': '14pt'}
        lbl1 = sortindex
        plot.setLabel("left", lbl1, **label_style)  
        plot.setLabel("bottom", "Sıralama",**label_style)

        sort_values = sorted(values, key = lambda i: i[sortindex])

        for value in sort_values:
            
            y = float(value[sortindex])  

            if value["Rank"] == findervalue[0]["Rank"]:
                bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush='b')
                self.xaxis = [b]
                self.yaxis = y
                plot.addItem(bg) 

            else:
                bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush=color[a])
                plot.addItem(bg) 

            tooltip = ""
            for key in value:
                if not key in self.bandict:
                    tooltip += key + ": " + str(value[key]) + "\n"
            bg.setToolTip(tooltip.strip())
            plot.addItem(bg)  

            if database != "MOTHERBOARD":
                text = pg.TextItem(text=value["Brand"]+" "+value["Model"] , color=(200, 200, 200),angle=0)
                text.setPos(b,y*1.05)
                plot.addItem(text)
            else:
                text = pg.TextItem(text=value["Brand"], color=(200, 200, 200), angle=0)
                text.setPos(b,y*1.05)
                plot.addItem(text)

            a += 1
            b += 1
            if a == 3:
                a = 0
        plot.setLimits(xMin = 0, xMax= b*1.1,yMin=-15)

        return plot

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(700)
    sys.exit(app.exec_())
