#!/bin/bash
# Recon smb with nmap
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${2} ]; then
    echo "Usage: ${0} <domain> <hostname>"
    exit
fi

# thinc.local
host -l ${1} ${2}

