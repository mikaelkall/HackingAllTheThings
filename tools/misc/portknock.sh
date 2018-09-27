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
    nmap -Pn --max-retries 0 -p "${PORT}" "${HOST}"
    sleep 0.5
done
