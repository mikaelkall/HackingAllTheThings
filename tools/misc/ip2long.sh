#!/bin/bash
if [ -z ${1} ]; then
    echo "Usage: ${0} <ip>"
    exit 1
fi

python3 -c "import ipaddress;print(int(ipaddress.IPv4Address('${1}')))"
