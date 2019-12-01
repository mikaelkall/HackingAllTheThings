#!/bin/bash
nmap --script http-webdav-scan -p80,443,8080 10.11.1.0/24
