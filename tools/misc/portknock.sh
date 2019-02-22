#!/bin/bash
# Simple nmap port knocking script.
# nighter@nighter.se

if [ -z ${2} ]; then
    echo "Usage: <host> <ports>"
    exit
fi

HOST="${1}"
shift

for PORT in "${@}";
do
    nmap -PN --max-retries 0 -p "${PORT}" "${HOST}"
    sleep 0.5
done

echo -e "\e[32m[+]\e[34m Checking for new ports with nmap ...\e[39m"
sleep 3
nmap -sT -p- -r -n $HOST --open | grep open
