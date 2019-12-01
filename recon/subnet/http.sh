#!/bin/bash
nmap -p 80,443,8080 10.11.1.0/24 --open -P0
