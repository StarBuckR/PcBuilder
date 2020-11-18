from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
import sys
import os

sys.path.insert(1, os.getcwd() + '/src/helpers/')
sys.path.insert(1, os.getcwd() + '/src/scripts/')

from builder import builder
from percentage import Percentage


if not os.path.exists("./fonts/OFL.txt"):
    import download_file as df
    df.download_fonts()

class elementBuilder(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(elementBuilder, self).__init__(*args, **kwargs)
        id_ = QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")

    def button_builder(self, content, width, height):
        temp_button = QPushButton()
        temp_button.setMaximumWidth(int(width))
        temp_button.setMinimumHeight(int(height))
        temp_button.setStyleSheet(
            "background-color:rgb(112,121,140);"
            "font-size:25px;"
        )
        temp_button.setText(content)
        return temp_button

    def combob_builder(self, width, height, content):
        temp_combo = QComboBox()
        temp_combo.addItem("Default")
        temp_combo.addItems(content)
        temp_combo.setMaximumWidth(width)
        temp_combo.setMinimumHeight(height)
        temp_combo.setStyleSheet(
            'font-size:18px')
        return temp_combo

    def label_b(self, content, font, size, alignment):
        temp_label = QLabel()
        temp_label.setText(content)
        temp_label.setAlignment(alignment)
        temp_label.setFont(QFont("Quantico", size))
        return temp_label

    def qlineE_b(self, width, height, alignment, validator):
        temp_qline = QLineEdit()
        temp_qline.setValidator(validator)
        temp_qline.setMaximumWidth(width)
        temp_qline.setMinimumHeight(height)
        temp_qline.setAlignment(Qt.AlignCenter)
        temp_qline.setStyleSheet("font-size:25px")
        return temp_qline

    def group_builder(self,head):
        temp_group = QGroupBox(head)
        temp_group.setStyleSheet(
            'font-size:20px')
        return temp_group

    def onRadioButtonClicked(self):
        radiobutton= self.sender()
        percentages=["33","28","15","10","10","5","8"]
        percentages_casual=["28","27","15","10","10","5","8"]
        if radiobutton.isChecked():
            self.pc_pp = radiobutton.text()
            if self.pc_pp == 'Gaming':
                for i,data in enumerate(self.edit_lines):
                    data.setText(percentages[i])
            else:
                for i,data in enumerate(self.edit_lines):
                    data.setText(percentages_casual[i])
            

class MainWindow(elementBuilder):

    def percentage_bar(self):
        last_bar = QHBoxLayout()
        elements=["CPU Price Percantage","GPU Price Percantage","Motherboard Price Percantage",\
            "RAM Price Percantage","SSD Price Percantage","HDD Price Percentage","Psu and Case Percentage"]
        percentages=["33","28","15","10","10","5","8"]
        self.edit_lines =[]
        for i,data in enumerate(elements):
            temp_hor = QHBoxLayout()
            temp_perc = QVBoxLayout()
            temp_perc.setAlignment(Qt.AlignCenter)
            temp_g = self.group_builder(data)
            edit_line = self.qlineE_b(int(self.width/7),
                                      int(self.height/40), Qt.AlignLeft, QIntValidator())
            self.edit_lines.append(edit_line)
            edit_line.setText(percentages[i])
            temp_hor.addWidget(edit_line)
            temp_hor.addWidget(QLabel('%'))
            temp_perc.addLayout(temp_hor)
            temp_g.setLayout(temp_perc)
            last_bar.addWidget(temp_g)
        return last_bar

    def purpose_layout(self):
        purpose = QHBoxLayout()
        purpose.setAlignment(Qt.AlignCenter)
        purpose.setSpacing(30)
        self.groupBox = self.group_builder('Purpose')

        self.radioGaming = QRadioButton("Gaming")
        self.radioGaming.clicked.connect(self.onRadioButtonClicked)
        
        self.radioDesktop = QRadioButton("Casual")
        self.radioDesktop.clicked.connect(self.onRadioButtonClicked)
        
        self.radioWorkstation = QRadioButton("Rendering")
        self.radioWorkstation.clicked.connect(self.onRadioButtonClicked)

        purpose.addWidget(self.radioGaming)
        purpose.addWidget(self.radioDesktop)
        purpose.addWidget(self.radioWorkstation)
        
        self.radioDesktop.setStyleSheet("QRadioButton{ font : 25px Quantico;}")
        self.radioDesktop.adjustSize()
        self.radioWorkstation.setStyleSheet("QRadioButton{ font : 25px Quantico;}")
        self.radioWorkstation.adjustSize()
        self.radioGaming.setStyleSheet("QRadioButton{ font : 25px Quantico;}")
        self.radioGaming.adjustSize()

        self.groupBox.setLayout(purpose)
        self.groupBox.setAlignment(Qt.AlignCenter)
        return self.groupBox

    def additional(self):
        group = self.group_builder('Additional')
        additional = QHBoxLayout()
        cpu = QVBoxLayout()
        gpu = QVBoxLayout()
        storage = QVBoxLayout()
        
        cpu.addWidget(self.label_b('CPU Brand',"Quantico",12,Qt.AlignLeft))
        self.cpu_brand_box =self.combob_builder(int(self.width/6), int(self.height/40), ['Intel', 'AMD'])
        cpu.addWidget(self.cpu_brand_box)

        gpu.addWidget(self.label_b('GPU Brand',"Quantico",12,Qt.AlignLeft))
        self.gpu_brand_box = self.combob_builder(int(self.width/6), int(self.height/40), ['Nvidia', 'AMD'])
        gpu.addWidget(self.gpu_brand_box)

        storage.addWidget(self.label_b('Storage Type',"Quantico",12,Qt.AlignLeft))
        self.storage_box = self.combob_builder(int(self.width/6), int(self.height/35), ['Only SSD', 'Only HDD'])
        storage.addWidget(self.storage_box)
        
        additional.addLayout(cpu)
        additional.addLayout(gpu)
        additional.addLayout(storage)
        
        group.setLayout(additional)
        return group

    def builded_pc(self,pcs):
        vertical_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        frame = QFrame()
        frame.setMinimumHeight(int(self.height/2))
        frame.setMinimumWidth(self.width)

        for pc in pcs:
            horizontal= QHBoxLayout()
            group_out = QGroupBox(pc['Title'])
            cpu = pc['CPU']['Brand']
    
            group_out.setLayout(horizontal)
            vertical_layout.addWidget(group_out)
        frame.setLayout(vertical_layout)
        scroll_area.setWidget(frame)
        return(scroll_area)
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Pc Builder")
        id_ = QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")
        self.setStyleSheet(
            "background-color:rgb(37,35,35);"
            "font-family:Quantico;"
            "color:rgb(245,241,237);")
        self.layout_vertical = QGridLayout() #main layout
        self.layout_vertical.setAlignment(Qt.AlignTop)
        
        layout_horizontal = QHBoxLayout()
        layout_f = QHBoxLayout()
        layout_s = QHBoxLayout()
        layout_t = QHBoxLayout()
        layout_label = QHBoxLayout()

        self.desktop = QApplication.desktop()  # Size setup
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.setGeometry(100, 100, int(self.width/32), int(self.height/18))

        self.budget_label = self.label_b(
            "MY BUDGET IS", "Arial", 45, Qt.AlignCenter)
        self.brand_label = self.label_b("Brand", "Quantico", 20, Qt.AlignLeft)
        self.pricepicker = self.qlineE_b(
            int(self.width/4), int(self.height /
                                   35), Qt.AlignCenter, QIntValidator())

        self.button = self.button_builder("BUILD IT", self.width/4, self.height/25)
        self.button.clicked.connect(self.add_pc)
        purpose = self.purpose_layout()
        additional = self.additional()
        layout_s.addWidget(self.pricepicker)
        layout_f.addWidget(purpose)
        layout_t.addWidget(self.button)
      
        self.layout_vertical.addWidget(self.budget_label, 0, 1)
        self.layout_vertical.addLayout(layout_s, 1, 1)
        self.layout_vertical.addLayout(layout_f, 2, 1)
        self.layout_vertical.addLayout(layout_label, 3, 1)
        self.layout_vertical.addLayout(self.percentage_bar(), 4, 1)
        self.layout_vertical.addWidget(additional,5,1)
        self.layout_vertical.addLayout(layout_t, 7, 1)

        widget = QWidget()
        widget.setLayout(self.layout_vertical)
        self.setCentralWidget(widget)
    
    def add_pc(self):
        if (self.radioDesktop.isChecked() or self.radioGaming.isChecked() or self.radioWorkstation.isChecked()) and \
            ((self.pricepicker.text() != "") and (int(self.pricepicker.text())>=550)):
            price = int(self.pricepicker.text())
            cpu_brand,gpu_brand,storage_type = self.control_brands()
            pc_type = self.pc_pp
           
            cpu,gpu,motherboard,ram,ssd,hdd,psu_and_case = self.getpercentages()
            pcs = builder(price,Percentage(cpu,gpu,motherboard,ram,ssd,hdd,psu_and_case),pc_type,gpu_brand,cpu_brand,storage_type)
            print(type(pcs))
            self.layout_vertical.addWidget(self.builded_pc(pcs),5,1)
        else:
            self.errorHandler('Please choose a PC Type')
    
    def control_brands(self):
        if self.gpu_brand_box.currentText() == "Default":
            gpu_brand = ["Nvidia", "AMD"]
        else:
            gpu_brand = [self.cpu_brand_box.currentText()]
        
        if self.gpu_brand_box.currentText() == "Default":
            cpu_brand = ["Intel","AMD"]
        else:
            cpu_brand = [self.cpu_brand_box.currentText()]
        
        if self.storage_box.currentText() == "Default":
            storage_type = ["Both"]
        elif self.storage_box.currentText() == "Only SSD":
            storage_type = ["OnlySSD"]
        else:
            storage_type = ["OnlyHDD"]
        
        return cpu_brand,gpu_brand,storage_type
    def getpercentages(self):
        cpu = int(self.edit_lines[0].text())
        gpu = int(self.edit_lines[1].text())
        motherboard = int(self.edit_lines[2].text())
        ram = int(self.edit_lines[3].text())
        ssd = int(self.edit_lines[4].text())
        hdd = int(self.edit_lines[5].text())
        psu_and_case = int(self.edit_lines[6].text())

        return cpu,gpu,motherboard,ram,ssd,hdd,psu_and_case

    def errorHandler(self,error):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(error)
        msgBox.setWindowTitle("There is a problem!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
