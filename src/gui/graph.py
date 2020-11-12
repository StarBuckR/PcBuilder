import pymongo
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from heapq import nlargest

win = pg.plot()
win.setWindowTitle('pyqtgraph example: BarGraphItem')
styles = {"color": "#f00", "font-size": "20px"}
win.setLabel("left", "Fiyat-Performans", **styles)
win.setLabel("bottom", "Sıralama", **styles)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["PcBuilder"]

class BarGraph(pg.BarGraphItem):
    def mouseClickEvent(self, event):
        print()

def createBarGraph(database, topindex, finderindex, number , name = None, brand = None):
    mycol = mydb[database]
    value = mycol.find({}, sort=[(topindex,-1)]).limit(number)

    a=0 #for changing colors
    b=0 #number
    x = np.arange(1) 
    color = ['b','y','g','r','d','w'] 
    for r in value:
        y = int(r[topindex])   
        bg = pg.BarGraphItem(x=x+b+1, height=y, width=0.3, brush=color[a])
        bgbtn = BarGraph(x=x+b+1, height=y, width=0.3, brush=color[a])
        win.addItem(bg)
        win.addItem(bgbtn)
        a += 1
        b += 1
        if a == 6:
            a = 0        

createBarGraph("RAM","MHZ","Rank",7)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
