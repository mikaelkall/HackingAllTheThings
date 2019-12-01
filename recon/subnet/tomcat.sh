#!/bin/bash
nmap --script=./tomcat-scan.nse 10.11.1.0/24 -p 8080
