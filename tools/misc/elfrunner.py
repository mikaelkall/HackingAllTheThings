#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
# ▓█████  ██▓      █████▒██▀███   █    ██  ███▄    █  ███▄    █ ▓█████  ██▀███                              #
# ▓█   ▀ ▓██▒    ▓██   ▒▓██ ▒ ██▒ ██  ▓██▒ ██ ▀█   █  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒                            #
# ▒███   ▒██░    ▒████ ░▓██ ░▄█ ▒▓██  ▒██░▓██  ▀█ ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒                            #
# ▒▓█  ▄ ▒██░    ░▓█▒  ░▒██▀▀█▄  ▓▓█  ░██░▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄                              #
# ░▒████▒░██████▒░▒█░   ░██▓ ▒██▒▒▒█████▓ ▒██░   ▓██░▒██░   ▓██░░▒████▒░██▓ ▒██▒                            #
# ░░ ▒░ ░░ ▒░▓  ░ ▒ ░   ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░                            #
# ░ ░  ░░ ░ ▒  ░ ░       ░▒ ░ ▒░░░▒░ ░ ░ ░ ░░   ░ ▒░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░                             #
# ░     ░ ░    ░ ░     ░░   ░  ░░░ ░ ░    ░   ░ ░    ░   ░ ░    ░     ░░   ░                                #
# ░  ░    ░  ░          ░        ░              ░          ░    ░  ░   ░                                    #
#                                                                                                           #
# elfrunner.py - nighter@nighter.se                                                                         #
#                                                                                                           #
# DATE                                                                                                      #
# 14/06/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# Execute local elf binaries directly from memory on remote server by pipe them over SSH                    #
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

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def create_perl_mem_payload():
    if os.path.isfile('%s' % BASEFILE) is False:
        print("%s does not exists" % BASEFILE)
        return False

    payload_file = '%s' % BASEFILE
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
open(my $FH, '>&='.$fd) or die "open: $!";
select((select($FH), $|=1)[0]);
'''
    with open(perl_payload_file, 'w') as f:
        f.write(payload)

    command = '''perl -e '$/=\\32;print"print \$FH pack q/H*/, q/".(unpack"H*")."/\ or die qq/write: \\$!/;\\n"while(<>)' %s >> %s''' % (payload_file, perl_payload_file)
    os.system(command)

    script_name = str(COMMAND.split(' ')[0]).split('/')[-1]
    arguments = '","'.join(COMMAND.split(' ')[1:])
    arguments = script_name + '","' + arguments

    payload = '''exec {"/proc/$$/fd/$fd"} "%s" or die "exec: $!";''' % arguments

    with open(perl_payload_file, 'a') as f:
        f.write(payload)


def ssh_execute():

    create_perl_mem_payload()
    command = "ssh -p %s %s@%s perl < /tmp/%s.pl" % (PORT, USER, IP, FILENAME)
    os.system(command)


def print_usage():
    print ("""
▓█████  ██▓      █████▒██▀███   █    ██  ███▄    █  ███▄    █ ▓█████  ██▀███  
▓█   ▀ ▓██▒    ▓██   ▒▓██ ▒ ██▒ ██  ▓██▒ ██ ▀█   █  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
▒███   ▒██░    ▒████ ░▓██ ░▄█ ▒▓██  ▒██░▓██  ▀█ ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
▒▓█  ▄ ▒██░    ░▓█▒  ░▒██▀▀█▄  ▓▓█  ░██░▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
░▒████▒░██████▒░▒█░   ░██▓ ▒██▒▒▒█████▓ ▒██░   ▓██░▒██░   ▓██░░▒████▒░██▓ ▒██▒
░░ ▒░ ░░ ▒░▓  ░ ▒ ░   ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ░  ░░ ░ ▒  ░ ░       ░▒ ░ ▒░░░▒░ ░ ░ ░ ░░   ░ ▒░░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
   ░     ░ ░    ░ ░     ░░   ░  ░░░ ░ ░    ░   ░ ░    ░   ░ ░    ░     ░░   ░ 
   ░  ░    ░  ░          ░        ░              ░          ░    ░  ░   ░     
[nighter@nighter.se]

Executes local elf binaries directly from memory on remote server by pipe them over SSH
    """)
    print "Usage: %s <USERNAME>@<HOST> <command>" % (sys.argv[0])
    print "\nEXAMPLE: elrunner.py 'username@127.0.0.1' HackingAllTheThings/tools/static/linux/x86_64/nmap 192.168.1.94 -p 80\n"
    sys.exit(0)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print_usage()

    HOST = sys.argv[1]
    COMMAND = sys.argv[2]

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

    BASEFILE = COMMAND.split(' ')[0]
    ssh_execute()

    # Cleanup
    try:
        os.unlink('/tmp/%s.pl' % FILENAME)
    except:
        pass