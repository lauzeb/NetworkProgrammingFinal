# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:10:40 2023

@author: Benjamin Lauze
"""


import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Port = 1234

s.bind(('',Port))
s.listen(30)

print("Server side")

while True:
    
   clientsocket, address = s.accept()
   
   while True:
    
       message = clientsocket.recv(2048).decode()
    
       print(f"Client: {message}")
    
       if (message == 'end'):
            break
    
       inputs = input("Server: ")
       clientsocket.send(inputs.encode())
    
       if (inputs == 'end'):
            break
               
   print("This is the conclusion of the session.")
    
   clientsocket.close()

s.close()