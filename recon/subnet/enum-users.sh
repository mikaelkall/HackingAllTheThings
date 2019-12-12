#!/bin/bash
nmap -sU -sS --script=smb-enum-users -p U:137,T:139 10.11.1.0/24 --open
