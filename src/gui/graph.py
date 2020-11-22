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

        self.layout = QVBoxLayout()

        # Initialize Tab Screen
        self.tabs = QTabWidget()

        # Adding Tabs With For Iteration
        for tab in range(0,6):       
            self.tab = QWidget()

            names = ["MOTHERBOARD","RAM","GPU","CPU","SSD","HDD"]
            self.tabs.addTab(self.tab,names[tab])
    
            self.tab_layout = QVBoxLayout(self)
            self.graph = self.createBarGraph(names[tab],"Price","Rank", 4)
            self.tab_layout.addWidget(self.graph)
            self.tab.setLayout(self.tab_layout)

        # Add Tabs To Widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.show()

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
        b=number #counter

        color = ['b','y','g','r','d','w','c','k']

        label_style = {'color': '#EEE', 'font-size': '14pt'}
        lbl1 = sortindex
        plot.setLabel("left", lbl1, **label_style)  
        plot.setLabel("bottom", "Low to high",**label_style)
        

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

            plot.addLegend()
            if database != "MOTHERBOARD":
                c2 = plot.plot(name=value["Brand"]+value["Model"],**label_style,pen=color[a])
            else:
                c2 = plot.plot(name=value["Brand"],**label_style,pen=color[a])
            
            a += 1
            b -= 1
            if a == 6:
                a = 0
        return plot
        
    # Changes Graph In The Tab    
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
