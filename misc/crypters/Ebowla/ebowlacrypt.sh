#!/bin/bash
# nighter@nighter.se
# Ebowla crypter wrapper.

SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}

function __puts()
{
    # Output messages in fancy colors.
    if [ "${1}" == "info" ]; then
	printf "%b%b%b\n" "\033[93m" "➜ " "${2}"
    elif [ "${1}" == "warning" ]; then
	printf "%b%b%b\n" "\033[93m" "➜ " "${2}"
    elif [ "${1}" == "error" ]; then
	printf "%b%b%b\n" "\033[91m" "✖ " "${2}"
    elif [ "${1}" == "success" ]; then
	printf "%b%b%b\n" "\033[92m" "✔ " "${2}"
    fi
}

main()
{
	[ ! -e './ebowla.py' ] && __puts 'error' 'Cannot find the ebowla.py' && exit
	[ ! -e "${1}" ] && __puts 'error' "Cannot find file to encrypt: ${1}" && exit

    FILENAME=$(basename "${1}")

    python2 ./ebowla.py "${1}" genetic.config
    ./build_x86_go.sh output/go_symmetric_${FILENAME}.go ${FILENAME}_ebowla.exe
   # cleanup
   sleep 1
   rm -f output/go_symmetric_${FILENAME}.go
}


####
## Entry point
####
NAME=$(basename "$0")
if [ "$NAME" == "ebowlacrypt.sh" ]; then

    if [ -z ${1} ]; then
        echo "Encrypts payload with Ebowla"
        echo "Usage: ${0} <filename>"
        exit
    fi

     main $@
 fi
