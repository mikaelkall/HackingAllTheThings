#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# Parses and display content from pcap files.
import sys
from scapy.all import *
from scapy2dict import to_dict
from terminaltables import AsciiTable


def parse_packet(packet_file):

    # rdpcap comes from scapy and loads in our pcap file
    packets = rdpcap(packet_file)

    table_data = [['src', 'dr', 'dst','data']]

    # Let's iterate through every packet
    for packet in packets:
        if packet.haslayer(TCP):
            d = to_dict(packet, strict=True)
            try:
                table_data.append([str(d['IP']['src']) + ':' + str(d['TCP']['sport']),'->', str(d['IP']['dst']) + ':' + str(d['TCP']['dport']),''])
            except:
                pass

            try:
                table_data.append(['','','',d['Raw']['load'].decode('utf-8')])
            except:
                pass

    table = AsciiTable(table_data)
    print(table.table)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]}: <filename>")
        sys.exit(0)

    try:
        parse_packet(sys.argv[1])
    except:
        pass
