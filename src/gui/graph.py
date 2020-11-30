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

class Graph(QWidget):
    
    # Main Page
    def __init__(self,pcs):
        super(QWidget, self).__init__()
        QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")
        #creating main page
        self.order_bool = True
        self.pcs = pcs

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
            "color:white;"
            )

        # Initialize Combobox Screen
        self.layout = QVBoxLayout()        
        self.box1 = QComboBox()
        self.box2 = QComboBox()
        self.box3 = QComboBox()
        self.box3.currentTextChanged.connect(self.initialize_pcs_ids)
        self.box2.currentTextChanged.connect(self.pull_bar_graph)
        self.box1.currentTextChanged.connect(self.update_second_box)

        self.bandict = ["URL","Url","Benchmark","_id","Ram Count","Total Price","Please Choose Part","Brand","Model","Socket","Chipset OC","Chipset","Gb","Atx"]
 
        self.pcs_title = []
        self.box3.addItem("Please Choose Title")

        for pc in pcs:
            self.box3.addItem(pc["Title"])
            self.pcs_title.append(pc["Title"])
       
        self.layout.addWidget(self.box3)
        self.layout.addWidget(self.box1)
        self.layout.addWidget(self.box2)

        self.button = QPushButton('Toggle Sorting Order', self)
        self.layout.addWidget(self.button) 
        self.button.setEnabled(False)
        self.box1.setEnabled(False)
        self.box2.setEnabled(False)

        pg.setConfigOption('background', (37,35,35))
        self.graph = pg.PlotWidget()
        self.layout.addWidget(self.graph)

        self.setLayout(self.layout)
        self.show()

    def initialize_pcs_ids(self, title_text):
        for value in range(len(self.pcs_title)):
            if self.pcs_title[value]==title_text:
                self.motherboard_id = self.pcs[value]["Motherboard"]["_id"]
                self.ram_id = self.pcs[value]["RAM"]["_id"]
                self.gpu_id = self.pcs[value]["GPU"]["_id"]
                self.cpu_id = self.pcs[value]["CPU"]["_id"]
                print(self.gpu_id)

                if self.pcs[value]["SSD"]:
                    self.ssd_id = self.pcs[value]["SSD"]["_id"]
                else:
                    self.ssd_id = None
                if self.pcs[value]["HDD"]:
                    self.hdd_id = self.pcs[value]["HDD"]["_id"]
                else:
                    self.hdd_id = None
                self.number = value

        self.box1.clear()
        if self.hdd_id == None:
            self.names = ["Please Choose Part","MOTHERBOARD","RAM","GPU","CPU","SSD"]
        elif self.ssd_id == None:
            self.names = ["Please Choose Part","MOTHERBOARD","RAM","GPU","CPU","HDD"]
        else:
            self.names = ["Please Choose Part","MOTHERBOARD","RAM","GPU","CPU","HDD","SSD"]

        self.box1.addItems(self.names)
        self.box1.setEnabled(True)
        self.box1.setCurrentText("Please Choose Part")
        self.box2.clear()
        self.layout.removeWidget(self.graph)
        self.graph = pg.PlotWidget()
        self.layout.addWidget(self.graph)
                
    def update_second_box(self):
        self.database = self.box1.currentText()
        text = self.box1.currentText()
        self.box2.clear()
        self.box2.setEnabled(False)

        if self.number == None:
            value = self.pcs[0]
        else: 
            value = self.pcs[self.number]
        tooltip = ""

        if text =="MOTHERBOARD":
            text = "Motherboard"
            
        if not value[text] in self.bandict:
            for keys in value[text]:
                if not keys in self.bandict:
                    self.box2.addItem(keys)
                    self.box2.setEnabled(True)

    def pull_bar_graph(self,text):
        self.sort_index = text

        if self.sort_index == "":
            pass
        else:
            self.layout.removeWidget(self.graph)
        if self.database == "MOTHERBOARD":
            self.finder_index = self.motherboard_id
        elif self.database == "RAM":
            self.finder_index = self.ram_id
        elif self.database == "GPU":
            self.finder_index = self.gpu_id
        elif self.database == "CPU":
            self.finder_index = self.cpu_id
        elif self.database == "SSD":
            self.finder_index = self.ssd_id
        elif self.database == "HDD":
            self.finder_index = self.hdd_id

        self.graph = self.create_bar_graph(self.database,self.sort_index,self.finder_index, 30, 1)
        self.layout.addWidget(self.graph)

    # Creating a Bar Graph 
    def create_bar_graph(self,database, sort_index, finder_index, number, sort_number):
        self.plot = pg.PlotWidget()
        self.plot.setStyleSheet("color:black;") 

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["PcBuilder"]
        mycol = mydb[database]

        finder_value = mycol.find({"_id": finder_index})

        if self.database == "GPU":
            finder_id_hex = int(str(finder_index),16)
            first_id_index = mycol.find_one({})
            first_id_hex = int(str(first_id_index["_id"]),16)
            skip_value = finder_id_hex-first_id_hex
            values = mycol.find({}, sort=[("Rank",1)]).limit(number).skip(skip_value)
            
        else:    
            item_rank = int(finder_value[0]["Rank"])
            skip_value = int(item_rank-(number/2))      
            skip_value = max(min(skip_value, 1000), 0)
            values = mycol.find({}, sort=[("Rank",1)]).limit(number).skip(skip_value)
            
        a=0 #for changing colors
        b=1 #counter

        color = ['y','w']

        label_style = {'color': '#EEE', 'font-size': '14pt'}
        lbl1 = sort_index
        self.plot.setLabel("left", lbl1, **label_style)  
        self.plot.setLabel("bottom", "Ranking",**label_style)

        if(sort_number == 1):
            sort_values = sorted(values, key = lambda i: i[sort_index])
        else: 
            sort_values = reversed(sorted(values, key = lambda i: i[sort_index]))

        for value in sort_values:

            y = float(value[sort_index])  
            for titlenumber in range(len(self.pcs_title)):
                colors = ['b','r','g']
                if database == "MOTHERBOARD":
                    if value["_id"] == self.pcs[titlenumber]["Motherboard"]["_id"]:
                        bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush=colors[titlenumber])
                        self.plot.addItem(bg) 
                    else:
                        bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush=color[a])
                        self.plot.addItem(bg) 
                else:
                    if database != None:
                        if value["_id"] == self.pcs[titlenumber][database]["_id"]:
                            bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush=colors[titlenumber])
                            self.plot.addItem(bg) 
                        else:
                            bg = pg.BarGraphItem(x=[b], height=y, width=0.3, brush=color[a])
                            self.plot.addItem(bg)

                tooltip = ""
                for key in value:
                    if not key in self.bandict:
                        tooltip += key + ": " + str(value[key]) + "\n"
                bg.setToolTip(tooltip.strip())        
                self.plot.addItem(bg)  
            if a == 1:
                if database != "MOTHERBOARD":
                    text = pg.TextItem(text=value["Brand"]+" "+value["Model"] , color=(200, 200, 200),angle=0)
                    text.setPos(b-0.54,a-1.05)
                    self.plot.addItem(text)
                else:
                    text = pg.TextItem(text=value["Brand"], color=(200, 200, 200), angle=0)
                    text.setPos(b-0.54,a-1.05)
                    self.plot.addItem(text)
            else:
                if database != "MOTHERBOARD":
                    text = pg.TextItem(text=value["Brand"]+" "+value["Model"] , color=(200, 200, 200),angle=0)
                    text.setPos(b-0.54,y*1.05)
                    self.plot.addItem(text)
                else:
                    text = pg.TextItem(text=value["Brand"], color=(200, 200, 200), angle=0)
                    text.setPos(b-0.54,y*1.05)
                    self.plot.addItem(text)

            a += 1
            b += 1
            if a == 2:
                a = 0
        self.plot.setLimits(xMin = 0, xMax= b,yMin=y*-1.05,yMax=y*1.5)

        self.button.setEnabled(True)   
        self.sort_number = sort_number
        self.button.clicked.connect(self.change_number) 

        return self.plot

    def change_number(self):
        self.order_bool = not self.order_bool
        self.plot.getViewBox().invertX(self.order_bool)

def graph_builder(pcs):
    window = Graph(pcs)
    window.show()
    app.exec_()
