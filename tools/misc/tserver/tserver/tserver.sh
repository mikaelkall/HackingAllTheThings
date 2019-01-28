#!/bin/bash
# Start tserver

SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}

# Settings
CONTAINER_NAME="tserver"

# Colors
RED="\e[91m"
GREEN="\e[32m"
RESET=$(tput sgr0)

function _container_is_up()
{
     local container=$@
     STATUS=$(docker inspect -f {{.State.Running}} ${container} 2>/dev/null)

     if [ ${#STATUS} == 0 ]; then
         STATUS='false'
     fi
}

function _check_status()
{
    _container_is_up "${CONTAINER_NAME}"
    if [[ "${STATUS}" == 'false' ]];
    then
        echo -e "[TSERVER]: ${RED}Stopped${RESET}"
    else
        echo -e "[TSERVER]: ${GREEN}Running${RESET}"
    fi
}

##
## MAIN
##
case "$1" in
    up)
       _container_is_up "${CONTAINER_NAME}"

        if [[ "${STATUS}" == 'false' ]];
        then
           echo -e "${GREEN}Starting gateway${RESET}"
           docker run --name ${CONTAINER_NAME} --net=host -d -P ${CONTAINER_NAME}:latest
        else
           _check_status
        fi
    ;;
    down)
         docker stop ${CONTAINER_NAME}
         docker rm ${CONTAINER_NAME}
    ;;
    build)
         docker build -t ${CONTAINER_NAME}:latest .
    ;;
    status)
        _check_status
    ;;
    *)
        echo "Usage: $0 <up|down|status|build>"
        exit 1
    ;;
esac
