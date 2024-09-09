import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget, QHBoxLayout, 
                            QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QFileDialog,
                            QMessageBox)

import pandas as pd

import maincode
import filepathgen as fg

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UIsetting()
    
    def UIsetting(self):
        self.setFixedSize(400, 600)
        self.table_widget = Interface(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class Interface(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.controls()
        self.full_path = ''

    def controls(self):
        # efine layouts and widgets
        self.layout = QVBoxLayout(self) #masterlayout
        self.layout_top = QHBoxLayout(self)
        self.layout_path = QHBoxLayout(self)
        self.layout_name = QHBoxLayout(self)
        self.find_excel = QPushButton('feed me!')
        self.conv_excel = QPushButton('konvertieren')
        self.conv_excel.setEnabled(False)
        self.path_label = QLabel('Pfad')
        self.path_label_txt = QLabel()
        self.excel_name_label = QLabel('Dateiname')
        self.excel_name = QLabel()
        # add widgets to layout
        self.layout_top.addWidget(self.find_excel)
        self.layout_top.addWidget(self.conv_excel)
        self.layout_path.addWidget(self.path_label)
        self.layout_path.addWidget(self.path_label_txt)
        self.layout_name.addWidget(self.excel_name_label)
        self.layout_name.addWidget(self.excel_name)
        # add layouts to masterlayout
        self.layout.addLayout(self.layout_top)
        self.layout.addLayout(self.layout_path)
        self.layout.addLayout(self.layout_name)
        # connect buttons to methods
        self.find_excel.clicked.connect(self.excelgrabber)
        self.conv_excel.clicked.connect(self.excelconverter)
    

    def excelgrabber(self):
        self.conv_excel.setEnabled(False)
        self.path_label_txt.setText('')
        self.excel_name.setText('')
        self.expath = QFileDialog.getOpenFileName(None,caption= 'open file', directory=fg.current_directory)
        if self.expath[0]:
            try:
                self.full_path = self.expath[0]
                self.dirpath, self.filename = os.path.split(self.full_path)
                self.df = pd.read_excel(self.expath[0], header=1)
                self.path_label_txt.setText(self.dirpath)
                self.excel_name.setText(self.filename)
                self.conv_excel.setEnabled(True)
            except ValueError:
                self.msg = QMessageBox(icon=Warning, text='keine Excel-Datei ausgewählt')
                self.msg.show()

    def excelconverter(self):
            maincode.Converter(self.full_path)

def main():
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()