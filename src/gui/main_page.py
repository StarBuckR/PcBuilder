from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
import sys
import os

sys.path.insert(1, os.getcwd() + '/src/helpers/')
sys.path.insert(1, os.getcwd() + '/src/scripts/')

from element_builder import elementBuilder
from build_pc import build_pc, BuildType, GpuBrand, CpuBrand, StorageType, get_benchmark_text
from percentage import Percentage
from builder import builder

if not os.path.exists("./fonts/OFL.txt"):
    import download_file as df
    df.download_fonts()

class MainWindow(elementBuilder):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #initial layout and style setup
        self.setWindowTitle("Pc Builder")
        QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")
        self.setStyleSheet(
            "background-color:rgb(37,35,35);"
            "font-family:Quantico;"
            "color:rgb(245,241,237);")
        self.layout_main = QGridLayout()  # main layout
        self.layout_main.setAlignment(Qt.AlignTop)
        layout_f = QHBoxLayout()
        layout_s = QHBoxLayout()
        layout_t = QHBoxLayout()
        layout_label = QHBoxLayout()
        self.desktop = QApplication.desktop()  # Size setup
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.setGeometry(100, 100, int(self.width/2), int(self.height/10))
        
        #adds label
        self.budget_label = self.label_b("MY BUDGET IS", 45)
        self.brand_label = self.label_b("Brand", 20, Qt.AlignLeft)
        self.pricepicker = self.qlineE_b(int(self.width/4), int(self.height /20), Qt.AlignCenter, QIntValidator())
        
        # Creates button
        self.button = self.button_builder(
            "BUILD IT", self.width/4, self.height/25)
        self.button.clicked.connect(self.add_pc)

        # Creates purpose and additional layouts
        purpose = self.purpose_layout()
        additional = self.additional()

        # to center widgets i added widgets to the horizontal layouts
        layout_s.addWidget(self.pricepicker)
        layout_f.addWidget(purpose)
        layout_t.addWidget(self.button)

        # Creates percentage label and value
        self.percentage_v = 100
        self.percentage_vl = self.label_b(
            str(self.percentage_v)+" %", 20, Qt.AlignCenter)

        # adds all widgets and layouts to main layout
        self.layout_main.addWidget(self.budget_label, 0, 1)
        self.layout_main.addLayout(layout_s, 1, 1)
        self.layout_main.addLayout(layout_f, 2, 1)
        self.layout_main.addLayout(layout_label, 3, 1)
        self.layout_main.addLayout(self.percentage_bar(), 4, 1)
        self.layout_main.addWidget(self.percentage_vl, 5, 1)
        self.layout_main.addWidget(additional, 6, 1)
        self.layout_main.addLayout(layout_t, 8, 1)

        #sets centrel widget as layout
        widget = QWidget()
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)

#---------------------------------------------------------------Layouts-------------------------------------------------#
    
    #this function creates percentage section
    def percentage_bar(self):
        last_bar = QHBoxLayout()
        elements = ["CPU Price Percantage", "GPU Price Percantage", "Motherboard Price Percantage",
                    "RAM Price Percantage", "SSD Price Percantage", "HDD Price Percentage", "Psu and Case Percentage"]
        self.percentages_gaming = ["22", "33", "12", "10", "10", "5", "8"]
        self.edit_lines = []
        for i, data in enumerate(elements):
            temp_hor = QHBoxLayout()
            temp_perc = QVBoxLayout()
            temp_perc.setAlignment(Qt.AlignCenter)
            temp_g = self.group_builder(data)
            edit_line = self.qlineE_b(int(self.width/7),
                                      int(self.height/40), Qt.AlignLeft, QIntValidator())
            edit_line.textChanged.connect(self.percentage_label_controller)
            self.edit_lines.append(edit_line)
            edit_line.setText(self.percentages_gaming[i])
            temp_hor.addWidget(edit_line)
            temp_hor.addWidget(QLabel('%'))
            temp_perc.addLayout(temp_hor)
            temp_g.setLayout(temp_perc)
            last_bar.addWidget(temp_g)
        return last_bar

    # This function creates purpose radio boxes
    def purpose_layout(self):
        purpose = QHBoxLayout()
        purpose.setAlignment(Qt.AlignCenter)
        purpose.setSpacing(30)
        groupBox = self.group_builder('Purpose')
        groupBox.setAlignment(Qt.AlignCenter)
        
        self.radioGaming = QRadioButton("Gaming")
        self.radioGaming.clicked.connect(self.onRadioButtonClicked)
        self.radioDesktop = QRadioButton("Casual")
        self.radioDesktop.clicked.connect(self.onRadioButtonClicked)
        self.radioWorkstation = QRadioButton("Rendering")
        self.radioWorkstation.clicked.connect(self.onRadioButtonClicked)
        
        purpose.addWidget(self.radioGaming)
        purpose.addWidget(self.radioDesktop)
        purpose.addWidget(self.radioWorkstation)
        
        self.radioDesktop.setStyleSheet("QRadioButton{ font-size: 25px ;}")
        self.radioDesktop.adjustSize()
        self.radioWorkstation.setStyleSheet("QRadioButton{ font-size: 25px ;}")
        self.radioWorkstation.adjustSize()
        self.radioGaming.setStyleSheet("QRadioButton{ font-size : 25px ;}")
        self.radioGaming.adjustSize()
        groupBox.setLayout(purpose)
        
        return groupBox

    def additional(self):
        group = self.group_builder('Additional')
        additional = QHBoxLayout()
        cpu = QVBoxLayout()
        gpu = QVBoxLayout()
        storage = QVBoxLayout()

        cpu.addWidget(self.label_b('CPU Brand', 12, Qt.AlignLeft))
        self.cpu_brand_box = self.combob_builder(int(self.width/6), int(self.height/40), ['Intel', 'AMD'])
        cpu.addWidget(self.cpu_brand_box)

        gpu.addWidget(self.label_b('GPU Brand', 12, Qt.AlignLeft))
        self.gpu_brand_box = self.combob_builder(int(self.width/6), int(self.height/40), ['Nvidia', 'AMD'])
        gpu.addWidget(self.gpu_brand_box)

        storage.addWidget(self.label_b('Storage Type', 12, Qt.AlignLeft))
        self.storage_box = self.combob_builder(int(self.width/6), int(self.height/35), ['Only SSD', 'Only HDD'])
        storage.addWidget(self.storage_box)

        additional.addLayout(cpu)
        additional.addLayout(gpu)
        additional.addLayout(storage)
        group.setLayout(additional)

        return group

    def builded_pc(self, pcs):
        # This function creates scroll area for builded pcs. Adds each of them verticaly in a frame. Every pc and pc parts have their own group.
        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(50)
        scroll_area = QScrollArea()
        scroll_area.setAlignment(Qt.AlignCenter)
        frame = QFrame()
        frame.setMinimumHeight(int(self.height/23))
        frame.setMinimumWidth(int(self.width/1.08))

        for pc in pcs:
            temp_vertical = QVBoxLayout()
            horizontal = QHBoxLayout()
            group_out = QGroupBox(pc['Title'])
            group_out.setStyleSheet("font-size:18px;")

            # to get needed data.
            left_over = str(round(pc['Leftover Price']))
            cpu = [pc['CPU']['Brand'], pc['CPU']['Model'], pc['CPU']['Price'],
                   pc['CPU'][get_benchmark_text(self.pc_pp)], pc['CPU']['Price-Performance']]
            gpu = [pc['GPU']['Brand'], pc['GPU']['Model'], pc['GPU']['Price'],
                   pc['GPU'][get_benchmark_text(self.pc_pp)], pc['GPU']['Price-Performance']]
            motherboard = [pc['Motherboard']['Brand'], pc['Motherboard']
                           ['Price'], pc['Motherboard']['MHZ'], pc['Motherboard']['Atx']]
            ram = [pc['RAM']['Brand'], pc['RAM']['Model'], pc['RAM']['Gb'], pc['RAM']
                   ['Price'], pc['RAM']['MHZ'], pc['RAM']['CL'], pc['RAM']['Price-Performance']]

            # PC CPU specs section
            cpu_group = QGroupBox('CPU')
            cpu_vertical = QVBoxLayout()
            cpu_vertical.addWidget(self.label_b(
                cpu[0]+" "+cpu[1], 15, Qt.AlignLeft))
            cpu_vertical.addWidget(self.label_b(get_benchmark_text(
                self.pc_pp)+": "+str(cpu[3]), 15, Qt.AlignLeft))
            cpu_vertical.addWidget(self.label_b(
                "Price Performance: "+str(round(cpu[4])), 15, Qt.AlignLeft))
            cpu_vertical.addWidget(self.label_b(
                str(cpu[2])+"$", 15, Qt.AlignLeft))
            cpu_group.setLayout(cpu_vertical)

            # PC GPU specs section
            gpu_group = QGroupBox('GPU')
            gpu_vertical = QVBoxLayout()
            gpu_vertical.addWidget(self.label_b(
                gpu[0]+" "+gpu[1], 15, Qt.AlignLeft))
            gpu_vertical.addWidget(self.label_b(get_benchmark_text(
                self.pc_pp)+": "+str(gpu[3]), 15, Qt.AlignLeft))
            gpu_vertical.addWidget(self.label_b(
                "Price Performance: "+str(round(gpu[4])), 15, Qt.AlignLeft))
            gpu_vertical.addWidget(self.label_b(
                str(gpu[2])+"$", 15, Qt.AlignLeft))
            gpu_group.setLayout(gpu_vertical)

            # PC motherboard specs section
            motherboard_group = QGroupBox('Motherboard')
            motherboard_vertical = QVBoxLayout()
            motherboard_vertical.addWidget(
                self.label_b(motherboard[0], 15, Qt.AlignLeft))
            motherboard_vertical.addWidget(self.label_b(
                str(motherboard[2])+" Mhz", 15, Qt.AlignLeft))
            motherboard_vertical.addWidget(
                self.label_b(motherboard[3], 15, Qt.AlignLeft))
            motherboard_vertical.addWidget(self.label_b(
                str(motherboard[1])+"$", 15, Qt.AlignLeft))
            motherboard_group.setLayout(motherboard_vertical)

            # PC RAM specs section
            ram_group = QGroupBox('RAM')
            ram_vertical = QVBoxLayout()
            ram_vertical.addWidget(self.label_b(
                ram[0]+" "+ram[1], 15, Qt.AlignLeft))
            ram_vertical.addWidget(self.label_b(
                ram[2]+" GB", 15, Qt.AlignLeft))
            ram_vertical.addWidget(self.label_b(
                str(ram[4])+" Mhz , CL: "+str(ram[5]), 15, Qt.AlignLeft))
            ram_vertical.addWidget(self.label_b(
                "Price Performance: "+str(round(ram[6])), 15, Qt.AlignLeft))
            ram_vertical.addWidget(self.label_b(
                str(ram[3])+"$", 15, Qt.AlignLeft))
            ram_group.setLayout(ram_vertical)

            # This section adds all group elements before ssd and hdd group elements because ssd or hdd group can be None
            horizontal.addWidget(cpu_group)
            horizontal.addWidget(gpu_group)
            horizontal.addWidget(motherboard_group)
            horizontal.addWidget(ram_group)

            if pc['SSD'] is not None:
                ssd = [pc['SSD']['Brand'], pc['SSD']['Model'], pc['SSD']['Storage'],
                       pc['SSD']['Price'], pc['SSD']['M2'], pc['SSD']['Price-Performance']]
                ssd_group = QGroupBox('SSD')
                ssd_vertical = QVBoxLayout()

                if ssd[2] >= 1000:
                    strg_v = round((ssd[2]/1000), 1)
                    strg = str(strg_v) + " TB"
                else:
                    strg = str(ssd[2])+" GB"
                
                ssd_vertical.addWidget(self.label_b(
                    ssd[0]+" "+ssd[1] + " M2" if ssd[4] == True else None, 15, Qt.AlignLeft))
                ssd_vertical.addWidget(self.label_b(strg, 15, Qt.AlignLeft))
                ssd_vertical.addWidget(self.label_b(
                    "Price Performance: "+str(round(ram[5])), 15, Qt.AlignLeft))
                ssd_vertical.addWidget(self.label_b(
                    str(ssd[3])+"$", 15, Qt.AlignLeft))
                ssd_group.setLayout(ssd_vertical)
                horizontal.addWidget(ssd_group)

            if pc['HDD'] is not None:
                hdd = [pc['HDD']['Brand'], pc['HDD']['Model'],
                       pc['HDD']['Storage'], pc['HDD']['Price']]
                hdd_group = QGroupBox('HDD')
                hdd_vertical = QVBoxLayout()
                if hdd[2] >= 1000:
                    strgh_v = round((hdd[2]/1000), 1)
                    strgh = str(strgh_v) + " TB"
                else:
                    strgh = str(hdd[2])+" GB"
                hdd_vertical.addWidget(self.label_b(
                    hdd[0]+" "+hdd[1], 15, Qt.AlignLeft))
                hdd_vertical.addWidget(self.label_b(strgh, 15, Qt.AlignLeft))
                hdd_vertical.addWidget(self.label_b(
                    str(hdd[3])+"$", 15, Qt.AlignLeft))
                hdd_group.setLayout(hdd_vertical)
                horizontal.addWidget(hdd_group)

            temp_vertical.addLayout(horizontal)
            temp_vertical.addWidget(self.label_b("Left:"+left_over+"$", 20))
            group_out.setLayout(temp_vertical)

            vertical_layout.addWidget(group_out)
        frame.setLayout(vertical_layout)
        scroll_area.setWidget(frame)
        return(scroll_area)

    #---------------------------------------------------------------Controllers-------------------------------------------------------------------#

    # Checks all conditions. If conditions meet calls builded_pc function and adds new layout
    def add_pc(self):
        if (self.radioDesktop.isChecked() or self.radioGaming.isChecked() or self.radioWorkstation.isChecked()) and \
                ((self.pricepicker.text() != "")):
            price = int(self.pricepicker.text())
            cpu_brand, gpu_brand, storage_type = self.control_brands()
            pc_type = self.pc_pp
            cpu, gpu, motherboard, ram, ssd, hdd, psu_and_case = self.getpercentages()
            if price > 550:
                if cpu+gpu+motherboard+ram+ssd+hdd+psu_and_case == 100:
                    pcs = builder(price, Percentage(gpu, cpu, ram, motherboard, ssd, hdd, psu_and_case), pc_type, gpu_brand, cpu_brand, storage_type)
                    self.layout_main.addWidget(self.builded_pc(pcs), 7, 1)
                else:
                    self.errorHandler(
                        "Summary of the percentages cannot be more or less than 100% ")
            else:
                self.errorHandler("Price cannot be lower than 550")
        else:
            self.errorHandler('Pc Type or Price cannot be empty')

    # Checks combo boxes current state
    def control_brands(self):
        if self.gpu_brand_box.currentText() == "Default":
            gpu_brand = GpuBrand.Both.value
        elif self.gpu_brand_box.currentText() == "AMD":
            gpu_brand = GpuBrand.AMD.value
        else:
            gpu_brand = GpuBrand.Nvidia.value

        if self.cpu_brand_box.currentText() == "Default":
            cpu_brand = CpuBrand.Both.value
        elif self.cpu_brand_box.currentText() == "AMD":
            cpu_brand = CpuBrand.AMD.value
        else:

            cpu_brand = CpuBrand.Intel.value
        if self.storage_box.currentText() == "Default":
            storage_type = StorageType.Both.value
        elif self.storage_box.currentText() == "Only SSD":
            storage_type = StorageType.OnlySSD.value
        else:
            storage_type = StorageType.OnlyHDD.value

        return cpu_brand, gpu_brand, storage_type

    # Gets current percentages.
    def getpercentages(self):
        cpu = int(self.edit_lines[0].text())
        gpu = int(self.edit_lines[1].text())
        motherboard = int(self.edit_lines[2].text())
        ram = int(self.edit_lines[3].text())
        ssd = int(self.edit_lines[4].text())
        hdd = int(self.edit_lines[5].text())
        psu_and_case = int(self.edit_lines[6].text())
        return cpu, gpu, motherboard, ram, ssd, hdd, psu_and_case

    # Raises error.
    def errorHandler(self, error):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(error)
        msgBox.setWindowTitle("There is a problem!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    # This function dynamically changes percentage label and warns user.
    def percentage_label_controller(self):
        temp_per = 0
        try:
            for i in range(len(self.edit_lines)):
                temp_per = temp_per + int(self.edit_lines[i].text())
            self.percentage_v = temp_per
            self.percentage_vl.setText(str(self.percentage_v)+"%")
            if self.percentage_v == 100:
                self.percentage_vl.setStyleSheet("color: white;")
            else:
                self.percentage_vl.setStyleSheet("color:red")
        except:
            pass

    # on any radio button clicked function set default percentages for selected pc type.
    def onRadioButtonClicked(self):
        radiobutton = self.sender()
        percentages_casual = ["28", "27", "12", "10", "10", "5", "8"]
        if radiobutton.isChecked():
            self.pc_pp = radiobutton.text()
            if self.pc_pp == 'Gaming':
                for i, data in enumerate(self.edit_lines):
                    data.setText(self.percentages_gaming[i])
                self.pc_pp = BuildType.Gaming.value
            elif self.pc_pp == 'Casual':
                for i, data in enumerate(self.edit_lines):
                    data.setText(percentages_casual[i])
                self.pc_pp == BuildType.Casual.value
            else:
                for i, data in enumerate(self.edit_lines):
                    data.setText(percentages_casual[i])
                self.pc_pp == BuildType.Rendering.value
                

def main_page():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
