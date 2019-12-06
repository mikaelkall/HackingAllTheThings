#!/bin/bash
WORDLIST="/usr/share/wordlist/SecLists/Passwords/Leaked-Databases/rockyou.txt"
hashcat -m 1000 -a 0 -o results.txt --remove ./hashes.hash "${WORDLIST}"
