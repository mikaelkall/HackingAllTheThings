#!/bin/bash
nmap -sU -sS --script smb-enum-shares.nse -p U:137,T:139,T:445 10.11.1.0/24 --open
