# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 15:27:43 2023

@author: Benjamin Lauze
"""

import socket

Port = 1234
Host ='127.0.0.1' #socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))
print("Client side")

s.sendall("STARTGAME".encode())
print("Password from server: ", s.recv(2048).decode())



'''
while True:
   
    inputs = input("Client ")
    s.sendall(inputs.encode())
    
    if (inputs == 'end'):
        break
    
    message = s.recv(2048).decode()
    
    
    print(f"Server: {message}")
    
    if (message == 'end'):
        break
 '''             
       
print("This is the conclusion of the session.")
  
#s.close()  
    
