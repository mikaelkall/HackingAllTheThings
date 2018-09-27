#!/bin/bash
# Windows base64 encode powershell compatible encoded string.

if [[ $# -eq 0 ]]; then
   cat | iconv --to-code UTF-16LE | base64 -w 0
else
   printf '%s' $1 | iconv --to-code UTF-16LE | base64 -w 0
fi
