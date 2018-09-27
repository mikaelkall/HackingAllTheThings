#!/usr/bin/env python2
import sys, urllib as ul;

if len(sys.argv) < 2:
    print "Usage: %s <url>" % sys.argv[0]
    sys.exit(0)

print(ul.unquote_plus(sys.argv[1]))
