#/bin/bash
nmap -p 80,443 10.11.1.0/24 --open -oG - | grep "/open" | awk '{ print $2  }'
