#!/bin/bash
# nighter@nighter.se
# Hyperion crypter wrapper.

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
	[ ! -e './hyperion.exe' ] && __puts 'error' 'Cannot find the hyperion.exe binary' && exit
	[ ! -e "${1}" ] && __puts 'error' "Cannot find file to encrypt: ${1}" && exit

	wine ./hyperion.exe "${1}" "{2}"
}

####                                                                                                                                                                                                                                         
## Entry point                                                                                                                                                                                                                               
####                                                                                                                                                                                                                                         
NAME=$(basename "$0")                                                                                                                                                                                                                        
if [ "$NAME" == "hypecrypt.sh" ]; then                                                                                                                                                                                                      
                                                                                                                                                                                                                                              
    if [ -z ${2} ]; then                                                                                                                                                                                                                     
        echo "Encrypts payload with Hyperion"                                                                                                                                                                                  
        echo "Usage: ${0} <filename> <outfile>"                                                                                                                                                                                                 
        exit                                                                                                                                                                                                                                 
    fi                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                              
     main $@                                                                                                                                                                                                                                  
 fi                                                               
