#!/usr/bin/env python2
import sys
import struct


def pattern_create(length):
    pattern = ''
    parts = ['A', 'a', '0']
    while len(pattern) != length:
        pattern += parts[len(pattern) % 3]
        if len(pattern) % 3 == 0:
            parts[2] = chr(ord(parts[2]) + 1)
            if parts[2] > '9':
                parts[2] = '0'
                parts[1] = chr(ord(parts[1]) + 1)
                if parts[1] > 'z':
                    parts[1] = 'a'
                    parts[0] = chr(ord(parts[0]) + 1)
                    if parts[0] > 'Z':
                        parts[0] = 'A'
    return pattern


def pattern_offset(value, buflen):
    if value.startswith('0x'):
        value = struct.pack('<I', int(value, 16)).strip('\x00')
    pattern = pattern_create(buflen)
    try:
        return pattern.index(value)
    except ValueError:
        return 'Not found'


def print_help():
    print 'Usage: %s (create | offset) <value> <buflen>' % sys.argv[0]


def main():
    if len(sys.argv) < 3 or sys.argv[1].lower() not in ['create', 'offset']:
        print_help()
        sys.exit(255)

    command = sys.argv[1].lower()
    num_value = sys.argv[2]

    if command == 'create':
        print pattern_create(int(num_value))
    else:
        if len(sys.argv) == 4:
            try:
                buflen = int(sys.argv[3])
            except ValueError:
                print_help()
                sys.exit(254)
        else:
            buflen = 8192
        print pattern_offset(num_value, buflen)

if __name__ == '__main__':
    main()

