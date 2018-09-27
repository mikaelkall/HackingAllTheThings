#!/bin/bash
# This script is a listner when you want to
# loot hardrive from a remote server.

PORT=5000
BACKUPDIR=/upload
DISK=sda

echo "Listening on: ${PORT} saving to ${BACKUPDIR}/${DISK}.img.gz"
nc -lp ${PORT} | sudo dd of=${BACKUPDIR}/${DISK}.img.gz
