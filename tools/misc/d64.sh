#!/bin/bash
if [[ $# -eq 0 ]]; then
    cat | base64 --decode
else
    printf '%s' $1 | base64 --decode
fi
