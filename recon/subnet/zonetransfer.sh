#!/bin/bash

NETWORK="10.11.1.0/24"
DOMAIN="thinc.local"

servers=$(nmap -p 53 ${NETWORK} --open -oG - | grep "/open" | awk '{ print $2 }')

for server in ${servers};
do
    echo "[*] zonetransfer: ${server}"
    host -l ${DOMAIN} ${server}
done
