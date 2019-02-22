#!/bin/bash
# Recon smb with nmap
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${2} ]; then
    echo "Username: ${0} <username> <address>"
    exit
fi

./ssh_user_enum --username ${1} ${2}
