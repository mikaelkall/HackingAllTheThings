#!/bin/bash
# nighter@nighter.se
# Serve payloads on serveral endpoints.

SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}

# SETTINGS
HTTP_PORT=8000
FTP_PORT=21
UPLOAD_PATH="/upload"
SMBSERVER="/usr/local/scripts/smbserver.py"
WEBDAVSERVER="/usr/local/scripts/webdav.py"

# Colors
RED="\e[91m"
GREEN="\e[32m"
YELLOW="\e[93m"
RESET=$(tput sgr0)

function CLEANUP_APPS
{
   echo -e "${RED}Stopping HTTP server${RESET}"
   kill -9 $(ps aux |grep "python3 -m http.server ${HTTP_PORT}" |grep -v "grep" |awk '{print $2}')  > /dev/null 2>&1
   echo -e "${RED}Stopping FTP server${RESET}"
   kill -9 $(ps aux |grep "python3 -m pyftpdlib -p ${FTP_PORT}" |grep -v "grep" |awk '{print $2}') > /dev/null 2>&1
   echo -e "${RED}Stopping SMB server${RESET}"
   kill -9 $(ps aux |grep "python2 ${SMBSERVER} UPLOAD ${UPLOAD_PATH}" |grep -v "grep" |awk '{print $2}') > /dev/null 2>&1
   echo -e "${RED}Stopping WEBDAV server${RESET}"
   kill -9 $(ps aux |grep "python2 ${WEBDAVSERVER}" |grep -v "grep" |awk '{print $2}') > /dev/null 2>&1

   exit 
}
trap CLEANUP_APPS EXIT

[ ! -e "${UPLOAD_PATH}" ] && mkdir -p "${UPLOAD_PATH}"
cd "${UPLOAD_PATH}"

echo -e "${YELLOW}--------------------------------------${RESET}"
echo -e "\t${RED}Serve HTTP${RESET}\t\t  "
echo -e "${YELLOW}--------------------------------------${RESET}"
python3 -m http.server ${HTTP_PORT} 2>/dev/null  &

for host in $(hostname -i);
do
   echo "http://${host}:${HTTP_PORT}/"
done

echo -e "${YELLOW}--------------------------------------${RESET}"
echo -e "\t${RED}Serve FTP(anonymous)${RESET}\t\t  "
echo -e "${YELLOW}--------------------------------------${RESET}"
python3 -m pyftpdlib -p ${FTP_PORT} 2>/dev/null &

for host in $(hostname -i);
do
   echo "ftp://anonymous:password@${host}:${FTP_PORT}/"
done

echo -e "\n"

echo -e "${YELLOW}--------------------------------------${RESET}"
echo -e "\t${RED}SMB server${RESET}\t\t  "
echo -e "${YELLOW}--------------------------------------${RESET}"
python2 ${SMBSERVER} UPLOAD ${UPLOAD_PATH} 2>/dev/null &

for host in $(hostname -i);
do
    echo "copy \\\\${host}\\UPLOAD\\filename ."
done

echo -e "\n"

echo -e "${YELLOW}--------------------------------------${RESET}"
echo -e "\t${RED}Starting WEBDAV server${RESET}\t\t  "
echo -e "${YELLOW}--------------------------------------${RESET}"
python2 ${WEBDAVSERVER} &

for host in $(hostname -i);
do
    echo "curl -T ./filename.txt http://${host}:8080/"
done

echo -e "\n"

sleep 1
echo "==================================================================="
# Bash spinner
i=1
sp="/-\|"
echo -e "\n\n"
echo -n ' '
while true; 
do
    printf "\b${sp:i++%${#sp}:1}"
    sleep 0.3
done 
