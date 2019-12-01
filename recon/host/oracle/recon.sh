#!/bin/bash
# Recon ORACLE with nmap
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${1} ]; then
    echo "Usage: ${0} <hostname>"
    exit
fi

# Setup paths to wordlists
SID_LIST1='/opt/metasploit/data/wordlists/sid.txt'
SID_LIST2='/usr/share/metasploit-framework/data/wordlists/sid.txt'

[ -e "${SID_LIST1}" ] && SID_LIST=${SID_LIST1}
[ -e "${SID_LIST2}" ] && SID_LIST=${SID_LIST2}

sudo nmap --script=oracle-sid-brute --script-args=oraclesids=${SID_LIST} -p 1521-1560 ${1} -P0
