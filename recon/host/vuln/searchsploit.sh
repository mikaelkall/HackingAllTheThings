#!/bin/bash
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${1} ]; then
    echo "Usage: ${0} <host>"
    exit
fi
nmap -p- -sV -oX a.xml ${1} ; searchsploit --nmap a.xml
