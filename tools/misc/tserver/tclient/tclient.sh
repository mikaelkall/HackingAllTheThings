#!/usr/bin/env bash
# Client script to be used on a Linux server.

# Address to the tunnel server
LHOST=127.0.0.1
LPORT=80
TPORT=445

ssh -nNT -R ${TPORT}:localhost:${TPORT} root@${LHOST} -p ${LPORT}