import pymongo
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import * 
import sys
from pyqtgraph.dockarea import *

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.win = pg.plot()
        self.win.setWindowTitle('pyqtgraph example: BarGraphItem')
        self.win.setStyleSheet(
            "background-color:rgb(37,35,35);"
            "color:black;")
           
    def createInfoLayout(self,info):
        if(info["Brand"] == " "):
            print(info["Brand"] + " " + info["Model"])
        else:
            print(info["Brand"])

    def createBarGraph(self,database, sortindex, finderindex, number , name = None, brand = None):

        bandict = ["URL","Url","Rank","Benchmark","Price-Performance","_id","Latency","Ram Count"]
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["PcBuilder"]
        mycol = mydb[database]
        values = mycol.find({}, sort=[(sortindex,-1)]).limit(number)
        a=0 #for changing colors
        b=0 #counter

        color = ['b','y','g','r','d','w','c','k']

        lbl1 = sortindex
  
        self.win.setLabel("left", lbl1)
        self.win.setLabel("bottom", "Ranking")

        for value in values:
            y = int(value[sortindex])   
            bg = pg.BarGraphItem(x=[b+1], height=y, width=0.3, brush=color[a])
            self.win.addItem(bg)   
            """c = self.win.plot(value, pen='w', symbol='o', symbolPen=color[a], symbolBrush=0.5, name="ANAN")"""        
            bgg = BarGraph(x=[b+1], height=y, width=0.3, brush=color[a])
            bgg.setinfos(value)

            tooltip = ""
            for deneme in value:
                if not deneme in bandict:
                    tooltip += deneme + ": " + str(value[deneme]) + "\n"
            
            bgg.setToolTip(tooltip.strip())

            self.win.addItem(bgg)  
            a += 1
            b += 1
            if a == 6:
                a = 0
            
    def on_click(self):
        print('PyQt5 button click')

class BarGraph(pg.BarGraphItem):
    def setinfos (self,info):
        self.info = info

    def mouseClickEvent(self, event):
        """print(self.info)"""
        Window.createInfoLayout(self,self.info)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()

    ex.createBarGraph("RAM","Price","Rank", 4)
    sys.exit(app.exec_())