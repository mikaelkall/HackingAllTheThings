#!/usr/bin/env python2
# python implementation of dsudo. This tool is inspired of sudo
# it executes command as root if you are part of the docker group.

import pexpect
import sys
import os

if len(sys.argv) < 2:
    print('dsudo <command>')
    sys.exit(0)

command = ' '.join(sys.argv[1:])

child = pexpect.spawn ('docker run --rm -v /:/mnt -i -t nighter/givemeroot')
child.timeout = 4

try:
    child.expect('sh-4.4#.*')
except:
    print("You need to be in docker group to have permissions on running docker.")
    sys.exit(0)

child.sendline('%s' % command)

try:
    child.expect('sh-4.4#.*')
except:
    print("You need to be in docker group to have permissions on running docker.")
    sys.exit(0)

child.sendline('end')
b=child.expect(['end'])
if b==0:
    print('\n'.join(str(child.before).split('\n')[1:-1]))
