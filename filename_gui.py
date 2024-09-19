import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget, QHBoxLayout, 
                            QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QFileDialog,
                            QMessageBox)

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UIsetting()
    
    def UIsetting(self):
        self.setFixedSize(300, 150)
        self.table_widget = Interface(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class Interface(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.controls()
        
    def controls(self):
        self.layout = QVBoxLayout(self) #masterlayout
        self.toplayout = QVBoxLayout(self)
        self.bottomlayout = QHBoxLayout(self)
        
        self.infotext = QLabel('Dateinamen eingeben (.xlsx wird automatisch ergänzt)')
        self.infotext.setWordWrap(True)
        self.filenametext = QLineEdit()
        self.ok = QPushButton('OK')
        self.cancel = QPushButton('Abbrechen')
        
        self.toplayout.addWidget(self.infotext)
        self.toplayout.addWidget(self.filenametext)
        self.bottomlayout.addWidget(self.ok)
        self.bottomlayout.addWidget(self.cancel)
        
        self.layout.addLayout(self.toplayout)
        self.layout.addLayout(self.bottomlayout)
    
        self.ok.clicked.connect(self.okbutton)
        self.cancel.clicked.connect(self.cancelbutton)
        
    def okbutton(self):
        self.filenametext.setText('wow, toll Du hast auf ok gedrückt')
    
    def cancelbutton(self):
        self.parent().close()
        
def main():
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
        