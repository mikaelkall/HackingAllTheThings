#!/usr/bin/python2
import sys

__author__ = 'kall.micke@gmail.com'

if len(sys.argv) < 2:
    print "Usage: %s <string>" % sys.argv[0]
    sys.exit(1)

input = sys.argv[1]

print 'String length : ' +str(len(input))
stringList = [input[i:i+4] for i in range(0, len(input), 4)]

for item in stringList[::-1] :
        print item[::-1] + ' : ' + str(item[::-1].encode('hex'))

for item in stringList[::-1]:
        print "push 0x"+str(item[::-1].encode('hex'))
