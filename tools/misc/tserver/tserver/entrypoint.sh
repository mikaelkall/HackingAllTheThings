#!/bin/sh

# generate host keys if not present
ssh-keygen -A

# sets a random root password
#ROOT_PASSWORD=$(date +%s | sha256sum | base64 | head -c 12 ; echo)
ROOT_PASSWORD=ZmY1NzkzMjhlYTFjZDU3ODA4Y2JmZT

# check wether a random root-password is provided
if [ ! -z ${ROOT_PASSWORD} ] && [ "${ROOT_PASSWORD}" != "root" ]; then
    echo "root:${ROOT_PASSWORD}" | chpasswd
    echo "ROOT PW: ${ROOT_PASSWORD}"
fi

# do not detach (-D), log to stderr (-e), passthrough other arguments
exec /usr/sbin/sshd -D -e "$@"
