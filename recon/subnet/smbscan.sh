#!/bin/bash
nmap -v -p 445 -Pn 10.11.1.0/24 --script=smb-os-discovery.nse -oG smb-scan.gnmap --open
