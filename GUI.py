#Manual downloads via GUI
#Scheduled downloads via text input

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtconsole.console import PythonConsole

from placeholders import connect_ftp

class FileDoctor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.centre()
        self.title = "FileDoctor"
        self.setWindowTitle(self.title)
        self.setMinimumSize(800, 500)
        self.tabWidget = Tabs(self)
        self.setCentralWidget(self.tabWidget)
        
        self.show()

    def centre(self):
        """centre the window upon launching app"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class Tabs(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(700,500)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Connection")
        self.tabs.addTab(self.tab2,"Download")
        self.tabs.addTab(self.tab3,"Schedule")
        
        # Create first tab CONNECTION
        self.tab1.layout = QGridLayout()

        #Input credentials
        self.hostLbl = QLabel(self)
        self.hostLbl.setText("Hostname:")
        self.userLbl = QLabel(self)
        self.userLbl.setText("Username:")
        self.pwdLbl = QLabel(self)
        self.pwdLbl.setText("Password:")
        
        self.hostField = QLineEdit(self)
        self.userField = QLineEdit(self)
        self.pwdField = QLineEdit(self)
        self.pwdField.setEchoMode(QLineEdit.Password)
        
        self.hostField.setFixedSize(300, 30)
        self.userField.setFixedSize(300, 30)
        self.pwdField.setFixedSize(300, 30)
        
        self.loginBtn = QPushButton("Login")
        self.loginBtn.clicked.connect(self.logIn)
        self.loginBtn.setFixedSize(QSize(100, 40))

        #Add widgets to tab 1
        self.tab1.layout.addWidget(self.hostLbl)
        self.tab1.layout.addWidget(self.hostField)
        self.tab1.layout.addWidget(self.userLbl)
        self.tab1.layout.addWidget(self.userField)
        self.tab1.layout.addWidget(self.pwdLbl)
        self.tab1.layout.addWidget(self.pwdField)
        self.tab1.layout.addWidget(self.loginBtn)
        self.tab1.setLayout(self.tab1.layout)
        
        #Create second tab DOWNLOAD
        self.tab2.layout = QGridLayout()

        #Calendar
        self.calLbl = QLabel(self)
        self.calLbl.setText("Choose a date and hit 'Download'")
        
        self.cal = QCalendarWidget(self)
        self.cal.setFixedSize(QSize(400, 300))
        
        self.cal.clicked[QDate].connect(self.showDate)
        date = self.cal.selectedDate()
        self.chosenDate = QLabel(self)
        self.chosenDate.setText(date.toString())

        self.downloadBtn = QPushButton("Download")
        self.downloadBtn.setFixedSize(QSize(80, 20))
        
        #Download Manually
        self.browseLbl = QLabel(self)
        self.browseLbl.setText("Or, browse for files to download manually:")
        self.browseLbl.move(0, 150)
        
        self.browseBtn = QPushButton("Browse...")
        self.browseBtn.setFixedSize(QSize(80, 20))
        
        #Add widgets to tab 2
        self.tab2.layout.addWidget(self.calLbl)
        self.tab2.layout.addWidget(self.chosenDate)
        self.tab2.layout.addWidget(self.downloadBtn)
        self.tab2.layout.addWidget(self.cal)
        self.tab2.layout.addWidget(self.browseLbl)
        self.tab2.layout.addWidget(self.browseBtn)
        self.tab2.setLayout(self.tab2.layout)
        
        #Create third tab SCHEDULE
        self.tab3.layout = QVBoxLayout()
        self.console = PythonConsole(self)
        self.console.eval_queued()
        self.console.push_local_ns('self.greet', self.greet)
        
        self.tab3.layout.addWidget(self.console)
        self.tab3.setLayout(self.tab3.layout)
        # Add tabs to window, and disable until successful login
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
    def greet():
        print("hello world")
    
    def showDate(self, date):
        """Show the currently selected date as text"""
        self.chosenDate.setText(date.toString())
        
    def logIn(self):
        """If login is successful, enable the other tabs"""
        hostname = self.hostField.text()
        username = self.userField.text()
        password = self.pwdField.text()

        try:
            connect_ftp(hostname, username, password)
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, True)
        except:
            raise
        #TODO link to placeholder ftp function
        #TODO connect to field input values
def testy():
    print("success")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDoctor()
    sys.exit(app.exec_())

