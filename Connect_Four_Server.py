#-*- coding: utf-8 -*-
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
            
            current_player.sendall(f"YOUR_TURN {self.game_board}".encode())
            
            # PLAYER SWAP VIA IF STATEMENT
            other_player = self.players[1] if current_player == self.players[0] else self.players[0]       
            other_player.sendall(f"WAITING_TURN {self.game_board}".encode())        
            
            # SYMBOL SWAP VIA IF STATEMENT
            symbol = 2 if current_player == self.players[1] else 1
            
            move = current_player.recv(2048).decode()
            self.moves(self,move,symbol)
            
            current_player = other_player
            
        winnerSocket = f"HOST_PLAYER_WON {self.game_board}" if current_player == self.players[1] else f"JOINING_PLAYER_WON {self.game_board}"
        
        self.players[0].sendall(f"{winnerSocket}".encode()) 
        self.players[1].sendall(f"{winnerSocket}".encode()) 
        
        self.endgameSequence()
        
            
    def moves(self, column, symbol):
        for row in range(len(self.game_board) - 1, -1, -1):           
            if self.game_board[row][column] == 0:
                self.game_board[row][column] = symbol
                currentWinCheck = self.winCheck(self)
                if currentWinCheck is not None:                    
                    self.game_active == False
                    return 
        return 
          
                
    def endgameSequence(self, clientsocket):        
      if self.players[0].recv(2048).decode() == "AGAIN_ACCEPTED" and self.players[1].recv(2048).decode() == "AGAIN_ACCEPTED":
           self.game_board = [[0 for _ in range(7)] for _ in range(6)] 
           self.activateGame(self)
      elif self.players[0].recv(2048).decode() == "CANCELGAME" or self.players[1].recv(2048).decode() == "CANCELGAME":
           self.players[0].sendall("FORCED_CANCEL".encode()) 
           self.players[1].sendall("FORCED_CANCEL".encode()) 
           self.game_active = False
           self.remove_game(self)
    
    def remove_game(self, game):
        if game in self.active_games:
            self.active_games.remove(game)
    
        
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
        
        
    def all_players_joined(players):
        return True if players[1] != None else False
    
    def password(self, clientsocket,password):
        try:
            for game in self.activeGames:
                if game.password == password:
                    if game.add_player(clientsocket):
                        clientsocket.sendall("PASSWORD_ACCEPTED".encode())
                        game.players[0].sendall("PASSWORD_ACCEPTED".encode())
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
        print(f"Closed Connection with client: {clientsocket}")
    
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
        for game in self.activeGames:
            if(game.players[0] == clientsocket):
                game.remove_game()  
                break
    
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
            try:
                message = clientsocket.recv(2048).decode()
                if not message:
                    break  # No more data received, exit the loop and thread
                self.respond(clientsocket, address, message)
            except Exception as e:
                print(f"Error: {e}. Socket has been closed closing thread")                
                break  # Socket likely closed, exit the loop and thread




                            
if __name__ == "__main__":
    server = ConnectFourServer(1234)
    server.start()
