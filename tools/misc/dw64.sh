#!/bin/bash
# Windows base64 decode powershell compatible encoded string
if [[ $# -eq 0 ]]; then
    cat | iconv --to-code UTF-8 | base64 -d
else
    printf '%s' $1 | iconv --to-code UTF-8 | base64 -d
fi
