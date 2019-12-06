#!/bin/bash
nmap -p21 --open --script=ftp-anon 10.11.1.0/24
