#!/bin/bash
nmap -sn -n --disable-arp-ping 10.11.1.0/24 -oG - | grep -i 'Up' | awk '{print $2}'
