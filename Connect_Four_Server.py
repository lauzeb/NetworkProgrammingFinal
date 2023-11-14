# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:27:43 2023

@author: Benjamin Lauze
"""
import gui
import socket
import threading
import random

class ConnectFourGameSession:
    def __init__(self, password, player1):
        self.password = password
        self.players = [player1, None]
        self.game_board = [[0] * 7 for _ in range(6)] #2d game board
        
    def add_player(self, player2_socket):
        if self.players[1] is None:
            self.players[1] = player2_socket
            return True  
        else:
            return False  

class ConnectFourServer:
    
    def __init__(self,port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.s.bind(('', self.port))
        self.s.listen(30)
        self.activeGames = []
        
        # Server main loop
    def start(self):
        print("Server side")
        while True:
            clientsocket, address = self.s.accept()
            print("New connection from client", address)
            newThread = threading.Thread(target=self.clientThread, args=(clientsocket, address))
            newThread.start()
    
        
    def startGame(self, clientsocket):
        password = random.randint(1000, 9999)
        while self.passwordInUse(password):
            password = random.randint(1000, 9999)

        newGame = ConnectFourGameSession(password, clientsocket)
        self.activeGames.append(newGame)
        clientsocket.sendall(str(password).encode())
        print("Started new game with password", password)
        
    def passwordInUse(self, password):
        for game in self.activeGames:
            if password == game.password:
                return True
        return False
    
    def passwordMatch(self,password): #called in JOIN GAME METHOD
        for game in self.activeGames:
            if(password == game.password):
                #connect users and active game
                return True # replace with ^
            
        raise Exception("invalid password") #GUI dialog box     
        
    def play(self, clientsocket):
        gui.open_dialog("StartOrJoinGame") 
    
    def joinGame(self, clientsocket):
        gui.open_dialog("TypeExistingPassword") 
    
    def password(self, clientsocket,password):
        pass  
    
    def exitGame(self, clientsocket):
        clientsocket.close() 
    
    def back(self, clientsocket):
        gui.open_dialog("MainMenu") 
    
    def again(self, clientsocket):
        gui.open_dialog("GameBoard")  
    
    def moves(self, clientsocket, column):
        pass  
    
    def winCheck(self):
        pass
        
    
    def respond(self,clientsocket, address, clientData):
        """
        Supported commands [WIP]:
            PLAY
            STARTGAME
            JOINGAME 
            PASSWORD [passwrd]
            EXITGAME
            BACK
            AGAIN
            -PLAYABLE MOVES [0 - 6]
        """
       
        commandData = clientData.split()
        command = commandData[0]
        
        match command:
            case "PLAY":
                self.play(clientsocket)
            case "STARTGAME":
                self.startGame(clientsocket)
            case "JOINGAME":
                self.joinGame(clientsocket)
            case "PASSWORD":
                self.password(clientsocket, commandData[1])
            case "EXITGAME":
                self.exitGame(clientsocket)
            case "BACK":
                self.back(clientsocket)
            case "AGAIN":
                self.again(clientsocket)
            case "MOVES":
                self.moves(clientsocket, commandData[1])
                          
    
    
    # Individual thread spawned for each connected client
    def clientThread(self, clientsocket, address):
        while True:
            message = clientsocket.recv(2048).decode()
            
            self.respond(clientsocket, address, message)
                            
if __name__ == "__main__":
    server = ConnectFourServer(1234)
    server.start()
