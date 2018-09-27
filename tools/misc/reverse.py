#!/usr/bin/env python2
import sys

__author__ = 'kall.micke@gmail.com'

if len(sys.argv) < 2:
    print "Usage: %s <string>" % sys.argv[0]
    sys.exit(1)

print str(sys.argv[1])[::-1]
