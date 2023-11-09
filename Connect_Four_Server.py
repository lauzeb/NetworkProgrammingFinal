# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:10:40 2023

@author: Benjamin Lauze
"""


import socket
import threading
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Port = 1234

s.bind(('',Port))
s.listen(30)

print("Server side")

activeGames = []

def startGame(clientsocket):
    password = random.randint(1000, 9999) #password random gen. If password is in use random gen again
    newGame = {
        'password': password,
        'player1': clientsocket
        }
    activeGames.append(newGame)
    clientsocket.sendall(str(password).encode())
    print("Started new game with password", password)
    

def respond(clientsocket, address, clientData):
    """
    Supported commands [WIP]:
        STARTGAME
        JOINGAME [passwd]
        EXITGAME
    """
   
    commandData = clientData.split()
    command = commandData[0]
    
    match command:
        case "STARTGAME":
           startGame(clientsocket)
        case "JOINGAME":
            pass
            #call joingame method
        
    

# Individual thread spawned for each connected client
def clientThread(clientsocket, address):
    while True:
        message = clientsocket.recv(2048).decode()
     
        respond(clientsocket, address, message)
                
        
# Server main loop
while True:
   clientsocket, address = s.accept()
   print("New connection from client", address)
   newThread = threading.Thread(target=clientThread, args=(clientsocket, address))
   newThread.start()
   


    
    
