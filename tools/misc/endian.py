#!/usr/bin/env python2
'''
Simple script to convert offset to little endian hex representation.
'''
import sys
import os

__author__ = 'kall.micke@gmail.com'

def print_usage():
    print("Usage: %s <offset>" % ( sys.argv[0] ))
    sys.exit(0)

if len(sys.argv) < 2:
    print_usage()
elif len(sys.argv[1])>10:
    print_usage()

mem=sys.argv[1]

if mem.startswith('0x'):
   mem = mem[2:]

result = ''
for (pos1, pos2) in reversed(zip(mem[0::2], mem[1::2])):
    result += '\\x%s%s' % (pos1, pos2)

print(result)
