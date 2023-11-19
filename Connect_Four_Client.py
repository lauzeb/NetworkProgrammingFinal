# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:27:43 2023

@author: Benjamin Lauze
"""

from PyQt5 import QtWidgets, uic, QtGui, QtCore
import socket
import sys

#port and default ip
Port = 1234
Host = socket.gethostname()

#socket creation and connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))
print("Client side")
        

class FirstPage(QtWidgets.QMainWindow):
    # default page ui
    def __init__(self):
        super(FirstPage, self).__init__()
        uic.loadUi('title.ui', self)
        
        self.playButton = self.findChild(QtWidgets.QPushButton, "playButton")
        self.playButton.clicked.connect(self.pressed_play)

        self.exitButton = self.findChild(QtWidgets.QPushButton, "exitButton")
        self.exitButton.clicked.connect(self.pressed_exit)
        
        #self.testLabel = self.findChild(QtWidgets.QLabel,"testLabel")
        
        self.show()
        
    def pressed_play(self):
        widget.setCurrentWidget(secondpage)
        
    def pressed_exit(self):
        s.sendall("EXITGAME".encode())
        s.close()
        widget.close()
        
class SecondPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(SecondPage, self).__init__()
        uic.loadUi('screen2.ui', self)
    
        self.createButton = self.findChild(QtWidgets.QPushButton, "createButton")        
        self.createButton.clicked.connect(self.pressed_create)
        
        self.joinButton = self.findChild(QtWidgets.QPushButton, "joinButton")        
        self.joinButton.clicked.connect(self.pressed_join)

        self.backButton = self.findChild(QtWidgets.QPushButton, "backButton")        
        self.backButton.clicked.connect(self.pressed_back)        
        
        self.show()

    def pressed_join(self):
        widget.setCurrentWidget(joinpage)
        # PULLS UP PASSWORD GUI
        # ASKS FOR PASSWORD
    
    def pressed_create(self):
        # SENDS STARTGAME 
        s.sendall("STARTGAME".encode())
        widget.setCurrentWidget(createpage)
        
    def pressed_back(self):
        widget.setCurrentWidget(firstpage)

class JoinPage(QtWidgets.QWidget):
    def __init__(self):
        super(JoinPage,self).__init__()
        uic.loadUi('joinPage.ui',self)
        
        self.enterPasswordButton = self.findChild(QtWidgets.QPushButton, "enterPasswordButton")
        self.enterPasswordButton.clicked.connect(self.pressed_enter_password)     
        
        self.backButton = self.findChild(QtWidgets.QPushButton, "backButton")        
        self.backButton.clicked.connect(self.pressed_back)     
        
        self.passwordEdit = self.findChild(QtWidgets.QLineEdit, "passwordEdit")
        
        self.errorLabel = self.findChild(QtWidgets.QLabel, "errorLabel")
                
        self.show()
    
    def pressed_enter_password(self):
        password = self.passwordEdit.text()
        s.sendall("PASSWORD {password}".encode())
        
        response = s.recv(2048).decode()
        
        if response == "PASSWORD_ACCEPTED":
            widget.setCurrentWidget(game_board)
        else:
            self.errorLabel.setEnabled(True)
            self.errorLabel.setText("Please try again. Error: {response}")
        
    def pressed_back(self):
        widget.setCurrentWidget(secondpage)
        

class CreatePage(QtWidgets.QWidget):
    
        
    def __init__(self):
        super(CreatePage,self).__init__()
        uic.loadUi('createPage.ui',self)
        
        self.cancelButton = self.findChild(QtWidgets.QPushButton, "cancelButton")        
        self.cancelButton.clicked.connect(self.pressed_cancel)     
                
        self.passwordLabel = self.findChild(QtWidgets.QLabel, "passwordLabel")
        
        self.game_logic = None
        """
        lobby_password = s.recv(2048).decode()
        
        self.passwordLabel.setText(str(lobby_password))
        
        somehow breaks UI HELP US 
        """
        self.show()
        """
        self.listen_for_password_accepted()
        """
        
    def pressed_cancel(self):
        s.sendall("CREATEBACK".encode())
        
        widget.setCurrentWidget(secondpage)
    """
    def listen_for_password_accepted(self):
        while True: 
            message = s.recv(2048).decode()
            if message == "PASSWORD_ACCEPTED":
                widget.setCurrentWidget(game_board)
      """          

class GameBoard(QtWidgets.QMainWindow):
    def __init__(self):
        super(GameBoard, self).__init__()
        uic.loadUi('gameBoard.ui', self)
        self.game_active = False
        self.players = [None, None]
        self.symbol = None
        self.current_player = None
        self.column_buttons = [self.findChild(QtWidgets.QPushButton, f"column{column}") for column in range(7)]

    def start_game(self):
        self.game_active = True
        self.current_player = self.players[0]
        self.symbol = 1  # Player 1 symbol

    def handlePlayerTurn(self):
        pass 
    
    def handleWaiting(self):
        pass

    def handleWin(self):
        pass
    
    def enable_all_buttons(self):
        for button in self.column_buttons:
            button.setEnabled(True)
    
    def disable_all_buttons(self):
        for button in self.column_buttons:
            button.setEnabled(False)

class GameLogic(QtCore.QObject):
        
    move_signal = QtCore.pyqtSignal()
    wait_signal = QtCore.pyqtSignal()
    win_signal = QtCore.pyqtSignal(str)
        
    def __init__(self,game_board):
        super().__init__()
        self.game_board = game_board
        self.game_active = False

    def start_game(self):
        # Start the game logic, set game_active to True, and begin the game loop
        self.game_active = True
        self.gameloop()
    
    
    def gameloop(self):
       while self.game_active:
           move = s.recv(2048).decode()
           
           match move:
               case "YOUR_TURN":
                   self.move_signal.emit()
               case "WAITING_TURN":
                   self.wait_signal.emit()
               # case for winner
               case default:
                   self.game_active = False
                   self.game_board.win_signal.emit()
               
       
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

firstpage = FirstPage()
secondpage = SecondPage()
joinpage = JoinPage()
createpage = CreatePage()
game_board = GameBoard()
game_logic = GameLogic(game_board)

widget.addWidget(firstpage)
widget.addWidget(secondpage)
widget.addWidget(joinpage)
widget.addWidget(createpage)
widget.addWidget(game_board)

game_logic.move_signal.connect(game_board.handlePlayerTurn)
game_logic.wait_signal.connect(game_board.handleWaiting)
game_logic.win_signal.connect(game_board.handleWin)

widget.setCurrentWidget(firstpage)


widget.show()
sys.exit(app.exec_())
    
