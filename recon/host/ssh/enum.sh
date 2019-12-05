#!/bin/bash
# SSH enum users from users.txt
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

[ ! -e './users.txt' ] && echo "[error] users.txt is missing" && exit

if [ -z ${1} ]; then
    echo "Usage: ${0} <hostname>"
    exit
fi

for username in $(cat ./users.txt); do
  ./check_user.sh "${username}" "${1}"
done

