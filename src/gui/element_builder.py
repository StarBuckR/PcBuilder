from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
import sys
import os

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
            "border-radius:12px")
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

    def label_b(self, content,size, alignment=Qt.AlignCenter):
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
        temp_qline.setStyleSheet(
            "font-size:25px;")
        return temp_qline

    def group_builder(self,head):
        temp_group = QGroupBox(head)
        temp_group.setStyleSheet(
            'font-size:20px')
        return temp_group
