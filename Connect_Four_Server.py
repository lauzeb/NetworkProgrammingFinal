# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:27:43 2023

@author: Benjamin Lauze
"""
import socket
import threading
import random

class ConnectFourGameSession:
    def __init__(self, password, player1):
        self.password = password
        self.players = [player1, None]
        self.game_board = [[0 for _ in range(7)] for _ in range(6)]
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
        
        current_player = self.players[0]
        symbol = 1 # PLAYER 1
        
        while self.game_active:
            current_player.sendall("YOUR_TURN".encode())
            
            # PLAYER SWAP VIA IF STATEMENT
            other_player = self.players[1] if current_player == self.players[0] else self.players[0]       
            other_player.sendall("WAITING_TURN".encode())        
            
            # SYMBOL SWAP VIA IF STATEMENT
            symbol = 2 if current_player == self.players[1] else 1
            
            move = current_player.recv(2048).decode()
            self.moves(self,move,symbol)
            
            current_player = other_player
            
        winnerSocket = "HOST_PLAYER_WON" if current_player == self.players[1] else "JOINING_PLAYER_WON"
        
        self.players[0].sendall(f"{winnerSocket}".encode()) 
        self.players[1].sendall(f"{winnerSocket}".encode()) 
        
        # TODO
        # AGAIN SEQUENCE
        
        
        
        
            
    def moves(self, column, symbol):
        for row in range(len(self.game_board) - 1, -1, -1):           
            if self.game_board[row][column] == 0:
                self.game_board[row][column] = symbol
                currentWinCheck = self.winCheck(self)
                if currentWinCheck is not None:                    
                    self.game_active == False
                    return 
        return 
    
    def again(self, clientsocket):
        if self.players[0].recv(2048).decode() == "AGAIN_ACCEPTED" and self.players[1].recv(2048).decode() == "AGAIN_ACCEPTED":
             self.game_board = [[0 for _ in range(7)] for _ in range(6)] 
             self.game_active = True
             
        
        
        

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
    
    def password(self, clientsocket,password):
        try:
            for game in self.activeGames:
                if game.password == password:
                    if game.add_player(clientsocket):
                        clientsocket.sendall("PASSWORD_ACCEPTED".encode())
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
    
    def cancelGame(self,clientsocket):
        if self.players[0].recv(2048).decode() == "CANCEL_ACCEPTED" or self.players[1].recv(2048).decode() == "CANCEL_ACCEPTED":
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

    def createBack(self, clientsocket):
       pass
       #todo
    
    def respond(self,clientsocket, address, clientData):
        """
        Supported commands [WIP]:
            -PLAY (CLIENT SIDE)
            STARTGAME
            JOINGAME 
            PASSWORD [passwrd]
            EXITGAME
            -BACK (CLIENT SIDE)
            AGAIN
            PLAYABLE MOVES [0 - 6]
        """
       
        commandData = clientData.split()
        command = commandData[0]
        
        match command:
            case "STARTGAME":
                self.startGame(clientsocket)
            case "PASSWORD":
                self.password(clientsocket, commandData[1])
            case "EXITGAME":
                self.exitGame(clientsocket)
            case "AGAIN":
                self.again(clientsocket)
            case "CANCELGAME":
                self.cancelGame(clientsocket)
            case "CREATEBACK":
                self.createBack(clientsocket)
                
    
    # Individual thread spawned for each connected client
    def clientThread(self, clientsocket, address):
        while True:
            message = clientsocket.recv(2048).decode()
            
            self.respond(clientsocket, address, message)
                            
if __name__ == "__main__":
    server = ConnectFourServer(1234)
    server.start()
