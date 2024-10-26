import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget, QHBoxLayout, 
                            QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QFileDialog,
                            QMessageBox, QCheckBox)

import pandas as pd

import maincode
import filepathgen as fg

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UIsetting()
    
    def UIsetting(self):
        self.setFixedSize(600, 400)
        self.table_widget = Interface(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class Interface(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.controls()
        self.thread = None
        self.full_path = ''

    def controls(self):
        # define layouts and widgets
        self.layout = QVBoxLayout(self) #masterlayout
        self.layout_top = QHBoxLayout(self)
        self.layout_path = QHBoxLayout(self)
        self.layout_name = QHBoxLayout(self)
        self.layout_check = QVBoxLayout(self)
        self.find_excel = QPushButton('feed me!')
        self.conv_excel = QPushButton('konvertieren')
        self.conv_excel.setEnabled(False)
        self.path_label = QLabel('Pfad')
        self.path_label_txt = QLabel()
        self.excel_name_label = QLabel('Dateiname')
        self.excel_name = QLabel()
        self.neworold = QCheckBox('Neuen Dateinamen nach Konvertierung verwenden')
        self.neworold.setEnabled(False)
        self.neworold.setChecked(False) #newname disabled by default
        self.newname = QLineEdit()
        self.newname.setEnabled(False)
        # add widgets to layout
        self.layout_top.addWidget(self.find_excel)
        self.layout_top.addWidget(self.conv_excel)
        self.layout_path.addWidget(self.path_label)
        self.layout_path.addWidget(self.path_label_txt)
        self.layout_name.addWidget(self.excel_name_label)
        self.layout_name.addWidget(self.excel_name)
        self.layout_check.addWidget(self.neworold)
        self.layout_check.addWidget(self.newname)
        # add layouts to masterlayout
        self.layout.addLayout(self.layout_top)
        self.layout.addLayout(self.layout_path)
        self.layout.addLayout(self.layout_name)
        self.layout.addLayout(self.layout_check)
        # connect buttons to methods
        self.find_excel.clicked.connect(self.excelgrabber)
        self.conv_excel.clicked.connect(self.excelconverter)
        self.neworold.stateChanged.connect(self.inputenabler)
    

    def excelgrabber(self):
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
                self.neworold.setEnabled(True)
            except ValueError:
                self.msg = QMessageBox(icon=Warning, text='keine Excel-Datei ausgewählt')
                self.msg.show()

    def excelconverter(self):
        if self.neworold.isChecked():
            if not self.newname.text():
                print('keine name')
            else:
                self.temptext = self.newname.text()
                maincode.Converter(self.full_path, self.temptext)   
        else:
            maincode.Converter(self.full_path, self.excel_name.text().rstrip('.xlsx'))

        

    def inputenabler(self, state):
        if state == 2:
            self.newname.setEnabled(True)
        else:
            self.newname.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()