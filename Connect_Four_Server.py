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
        self.game_active = False  # Indicates whether the game is active
        
    def add_player(self, player2_socket):
        if self.players[1] is None:
            self.players[1] = player2_socket
            return True  
        else:
            return False 
        
    def activateGame(self):
        self.game_active = True
        # Notify both players that the game has started
        for player_socket in self.players:
            if player_socket is not None:
                  player_socket.sendall("Game has started. Make your move.".encode())
        

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
        
        
    def all_players_joined(players):
        for player in players:
            if player is None:
                return False
            return True

        
    def play(self, clientsocket):
        gui.open_dialog("StartOrJoinGame") 
    
    def joinGame(self, clientsocket):
        gui.open_dialog("TypeExistingPassword") 
    
    def password(self, clientsocket,password):
        try:
            for game in self.activeGames:
                if game.password == password:
                    if game.add_player(clientsocket):
                        clientsocket.sendall("Password accepted. Joined game.".encode())
                        if self.all_players_joined(game.players):
                            game.activate_game()

                        return 
                    else:
                        clientsocket.sendall("Game is full.".encode())
                        return 
            clientsocket.sendall("Invalid password.".encode())
        except Exception:
            clientsocket.sendall("Illegal password, please try again.".encode())
            
  
    
    def exitGame(self, clientsocket):
        clientsocket.close() 
    
    def back(self, clientsocket):
        gui.open_dialog("MainMenu") 
    
    def again(self, clientsocket):
        gui.open_dialog("GameBoard")  
    
    def moves(self, column, game, player_symbol):
        try:
             for slot in game.game_board[column]:
                 if slot == 0:
                     game.game_board[column][slot] = player_symbol
                     self.winCheck(game)
                         #if !None:
                             
                             #a win has occurred, come back tot this later
                     return
#write this to make it work on both sides for exception                 
        except Exception:
            #game.currentplayer.sendall("Illegal move".encode())
            pass
        
        
#check this again later      
    def winCheck(self, game):
        # Check horizontal lines
       for row in self.game_board:
           for col in range(4):
               if row[col] != 0 and row[col] == row[col + 1] == row[col + 2] == row[col + 3]:
                   return row[col]

       # Check vertical lines
       for col in range(7):
           for row in range(3):
               if self.game_board[row][col] != 0 and self.game_board[row][col] == self.game_board[row + 1][col] == self.game_board[row + 2][col] == self.game_board[row + 3][col]:
                   return self.game_board[row][col]

       # Check diagonal (down-right and up-right)
       for col in range(4):
           for row in range(6):
               # Down-right
               if row < 3 and self.game_board[row][col] != 0 and self.game_board[row][col] == self.game_board[row + 1][col + 1] == self.game_board[row + 2][col + 2] == self.game_board[row + 3][col + 3]:
                   return self.game_board[row][col]
               # Up-right
               if row > 2 and self.game_board[row][col] != 0 and self.game_board[row][col] == self.game_board[row - 1][col + 1] == self.game_board[row - 2][col + 2] == self.game_board[row - 3][col + 3]:
                   return self.game_board[row][col]

       # No winner yet
       return None

        
    
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
