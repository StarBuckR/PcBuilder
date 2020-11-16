from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
import sys
import os

sys.path.insert(1, os.getcwd() + '/src/helpers/')

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
        temp_button.setText(content)
        return temp_button

    def combob_builder(self, width, height, content):

        temp_combo = QComboBox()
        temp_combo.addItem("Default")
        temp_combo.addItems(content)
        temp_combo.setMaximumWidth(width)
        temp_combo.setMinimumHeight(height)

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
        return temp_qline

    def spinbox_b(self, width, height):
        temp_sp = QSpinBox()
        temp_sp.setMaximumWidth(width)
        temp_sp.setMinimumHeight(height)
        return temp_sp


class MainWindow(elementBuilder):

    def storage_layout(self):
        group = QGroupBox("STORAGE")
        stg_l = QVBoxLayout()
        stg_l.setSpacing(20)
        stg_l.addWidget(self.label_b(
            'Storage Size', 'Arial', 20, Qt.AlignLeft))
        stg_l.addWidget(self.spinbox_b(
            int(self.width/5), int(self.height/16)))
        ssd = QRadioButton("ONLY SSD")
        hdd = QRadioButton("ONLY HDD")
        stg_l.addWidget(ssd)
        stg_l.addWidget(hdd)
        stg_l.addWidget(self.label_b(
            'Price Percantage', 'Arial', 20, Qt.AlignLeft))
        stg_l.addWidget(self.qlineE_b(int(self.width/5),
                                      int(self.height/25), Qt.AlignLeft, QIntValidator()))
        stg_l.setAlignment(Qt.AlignBottom)
        group.setLayout(stg_l)
        return group

    def mothearboard_layout(self):
        group = QGroupBox("MOTHERBOARD")
        mb_l = QVBoxLayout()
        mb_l.addWidget(self.label_b(
            'Price Percantage', 'Arial', 20, Qt.AlignLeft))
        mb_l.addWidget(self.qlineE_b(int(self.width/5),
                                     int(self.height/25), Qt.AlignLeft, QIntValidator()))
        mb_l.setAlignment(Qt.AlignBottom)
        group.setLayout(mb_l)
        return group

    def gpu_layout(self):
        group = QGroupBox("GPU")
        gpu_l = QVBoxLayout()
        gpu_l.addWidget(self.label_b('Brand', 'Arial', 20, Qt.AlignLeft))
        gpu_l.addWidget(self.combob_builder(
            int(self.width/5), int(self.height/16), ['Nvidia', 'AMD']))
        gpu_l.addWidget(self.label_b(
            'Price Percantage', 'Arial', 20, Qt.AlignLeft))
        gpu_l.addWidget(self.qlineE_b(int(self.width/5),
                                      int(self.height/25), Qt.AlignLeft, QIntValidator()))
        gpu_l.setAlignment(Qt.AlignBottom)
        group.setLayout(gpu_l)
        return group

    def cpu_layout(self):
        cpu_l = QVBoxLayout()
        group = QGroupBox("CPU")
        cpu_l.addWidget(self.label_b('Brand', 'Arial', 20, Qt.AlignLeft))
        cpu_l.addWidget(self.combob_builder(
            int(self.width/5), int(self.height/16), ['Intel', 'AMD']))
        cpu_l.addWidget(self.label_b(
            'Price Percantage', 'Arial', 20, Qt.AlignLeft))
        cpu_l.addWidget(self.qlineE_b(int(self.width/5),
                                      int(self.height/25), Qt.AlignLeft, QIntValidator()))
        cpu_l.setAlignment(Qt.AlignBottom)
        group.setLayout(cpu_l)
        return group

    def ram_layout(self):
        ram_l = QVBoxLayout()
        group = QGroupBox("RAM")
        ram_l.addWidget(self.label_b(
            'Price Percantage', 'Arial', 20, Qt.AlignLeft))
        ram_l.addWidget(self.qlineE_b(int(self.width/5),
                                      int(self.height/25), Qt.AlignLeft, QIntValidator()))
        ram_l.setAlignment(Qt.AlignBottom)
        group.setLayout(ram_l)
        return group

    def purpose_layout(self):
        purpose = QHBoxLayout()
        purpose.setAlignment(Qt.AlignCenter)
        purpose.setSpacing(30)
        self.groupBox = QGroupBox("Purpose")

        self.radioGaming = QRadioButton("Gaming")

        self.radioDesktop = QRadioButton("Desktop")

        self.radioWorkstation = QRadioButton("Workstation")

        purpose.addWidget(self.radioGaming)
        purpose.addWidget(self.radioDesktop)
        purpose.addWidget(self.radioWorkstation)

        self.groupBox.setLayout(purpose)
        self.groupBox.setAlignment(Qt.AlignCenter)
        return self.groupBox

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Pc Builder")
        id_ = QFontDatabase.addApplicationFont("./fonts/Quantico-Bold.ttf")
        self.setStyleSheet(
            "background-color:rgb(53,53,53);"
            "font-family:Quantico;"
            "color:white;"
        )

        layout = QHBoxLayout()
        layout_vertical = QGridLayout()
        layout_last = QVBoxLayout()
        layout_horizontal = QHBoxLayout()
        layout_f = QHBoxLayout()
        layout_s = QHBoxLayout()
        layout_t = QHBoxLayout()
        layout_label = QHBoxLayout()

        layout_vertical.setAlignment(Qt.AlignCenter)

        self.desktop = QApplication.desktop()  # Size setup
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.setGeometry(100, 100, int(self.width/32), int(self.height/18))

        self.budget_label = self.label_b(
            "MY BUDGET IS", "Arial", 68, Qt.AlignCenter)
        self.brand_label = self.label_b("Brand", "Quantico", 20, Qt.AlignLeft)
        self.pricepicker = self.qlineE_b(
            int(self.width/2), int(self.height /
                                   15), Qt.AlignCenter, QIntValidator()
        )

        self.pricepicker.setContentsMargins(200, 20, 200, 2)

        purpose = self.purpose_layout()

        stg_l = self.storage_layout()
        cpu_l = self.cpu_layout()
        mb_l = self.mothearboard_layout()
        ram_l = self.ram_layout()
        gpu_l = self.gpu_layout()

        layout_horizontal.addWidget(cpu_l)
        layout_horizontal.addWidget(gpu_l)
        layout_horizontal.addWidget(mb_l)
        layout_horizontal.addWidget(ram_l)
        layout_horizontal.addWidget(stg_l)
        layout_horizontal.setContentsMargins(70, 100, 70, 20)
        layout_horizontal.setSpacing(50)

        button = self.button_builder("BUILD IT", self.width/4, self.height/25)

        layout_s.addWidget(self.pricepicker)
        layout_f.addWidget(purpose)
        layout_t.addWidget(button)

        layout_vertical.addWidget(self.budget_label, 0, 1)
        layout_vertical.addLayout(layout_s, 1, 1)
        layout_vertical.addLayout(layout_f, 2, 1)
        layout_vertical.addLayout(layout_label, 3, 1)
        layout_vertical.addLayout(layout_horizontal, 4, 1)
        layout_vertical.addLayout(layout_t, 5, 1)

        widget = QWidget()
        widget.setLayout(layout_vertical)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
