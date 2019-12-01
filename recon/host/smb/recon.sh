#!/bin/bash
# Recon smb with nmap
SCRIPT_DIR=$(dirname $0)
cd ${SCRIPT_DIR}
SCRIPT_BASE=$(pwd)

if [ -z ${1} ]; then
    echo "Usage: ${0} <hostname>"
    exit
fi

sudo nmap -p445 --script=smb-os-discovery.nse ${1} -P0
sudo nmap -p445 --script=smb-vuln-ms17-010 ${1} -P0
sudo nmap -p445 --script=mb-vuln-ms10-061 ${1} -P0
sudo nmap -p445 --script=smb-vuln-ms10-054.nse --script-args unsafe ${1} -P0
sudo nmap -p445 --script=smb-vuln-ms08-067.nse ${1} -P0
sudo nmap -p445 --script=smb-vuln-ms07-029.nse ${1} -P0
sudo nmap -p445 --script=smb-vuln-ms06-025.nse ${1} -P0
sudo nmap -sU -p U:137 --script=smb-vuln-ms08-067.nse ${1} -P0

sudo nmap -p U:137,T:139 --script=smb-vuln-ms07-029.nse ${1} -P0
sudo nmap -p U:137,T:139,T:445 --script=smb-vuln-ms06-025.nse ${1} -P0

sudo nmap -p445 --script=smb-enum-shares.nse ${1} -P0
sudo nmap -p445 --script=smb-ls --script-args 'share=c$,pnath=\temp'
sudo nmap -p445 --script=smb-enum-users.nse ${1} -P0

sudo nmap -p445 --script smb2-vuln-uptime --script-args smb2-vuln-uptime.skip-os=true ${1} -P0

