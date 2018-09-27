#!/bin/bash

if [[ $# -eq 0 ]]; then
    cat | base64
else
    printf '%s' $1 | base64
fi
