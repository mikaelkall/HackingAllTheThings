#!/bin/bash
nmap -p445,139 --script=smb-vuln-ms08-067.nse 10.11.1.0/24 -P0
