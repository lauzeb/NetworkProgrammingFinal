# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:27:43 2023

@author: Benjamin Lauze
"""

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
import socket
import sys

Port = 1234
Host ='127.0.0.1' #socket.gethostname()
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((Host, Port))
print("Client side")
        
#s.sendall("STARTGAME".encode())
#print("Password from server: ", s.recv(2048).decode())
        
#secondpage = None


class FirstPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(FirstPage, self).__init__()
        uic.loadUi('title.ui', self)
        
        self.playButton = self.findChild(QtWidgets.QPushButton, "playButton")
        self.playButton.clicked.connect(self.PressedPlay)

        self.exitButton = self.findChild(QtWidgets.QPushButton, "exitButton")
        self.exitButton.clicked.connect(self.PressedExit)
        
        #self.testLabel = self.findChild(QtWidgets.QLabel,"testLabel")
        
        self.show()
        
    def PressedPlay(self):
        widget.setCurrentWidget(secondpage)
        
    def PressedExit(self):
        #s.sendall("EXITGAME".encode())
        s.close()
        widget.close()
        
class SecondPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(SecondPage, self).__init__()
        uic.loadUi('screen2.ui', self)
    
        self.createButton = self.findChild(QtWidgets.QPushButton, "createButton")        
        self.createButton.clicked.connect(self.PressedCreate)
        
        self.joinButton = self.findChild(QtWidgets.QPushButton, "joinButton")        
        self.joinButton.clicked.connect(self.PressedJoin)

        self.backButton = self.findChild(QtWidgets.QPushButton, "backButton")        
        self.backButton.clicked.connect(self.PressedBack)        
        
        self.show()

    def PressedJoin(self):
        widget.setCurrentWidget(joinpage)
        # PULLS UP PASSWORD GUI
        # ASKS FOR PASSWORD
    
    def PressedCreate(self):
        pass
        # SENDS STARTGAME 
        
    def PressedBack(self):
        widget.setCurrentWidget(firstpage)

class JoinPage(QtWidgets.QWidget):
    def __init__(self):
        super(JoinPage,self).__init__()
        uic.loadUi('joinPage.ui',self)
        
        self.enterPasswordButton = self.findChild(QtWidgets.QPushButton, "enterPasswordButton")
        self.enterPasswordButton.clicked.connect(self.PressedEnterPassword)     
        
        self.backButton = self.findChild(QtWidgets.QPushButton, "backButton")        
        self.backButton.clicked.connect(self.PressedBack)     
        
        self.passwordEdit = self.findChild(QtWidgets.QLineEdit, "passwordEdit")

        self.show()
    
    def PressedEnterPassword(self):
        password = self.passwordEdit.text()
        #s.sendall("PASSWORD {password}".encode())
        pass
    
    def PressedBack(self):
        widget.setCurrentWidget(secondpage)

        
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

firstpage = FirstPage()
secondpage = SecondPage()
joinpage = JoinPage()

widget.addWidget(firstpage)
widget.addWidget(secondpage)
widget.addWidget(joinpage)

widget.setCurrentWidget(firstpage)


widget.show()
sys.exit(app.exec_())
    
