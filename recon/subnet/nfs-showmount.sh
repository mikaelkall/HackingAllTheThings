#!/bin/bash
nmap -sV -p 111 --script=nfs-showmount 10.11.1.0/24 --open
