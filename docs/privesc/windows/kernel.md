## Run exploit suggester against systeminfo:

https://github.com/GDSSecurity/Windows-Exploit-Suggester/blob/master/windows-exploit-suggester.py

```sh
$ python windows-exploit-suggester.py -d 2017-05-27-mssb.xls -i systeminfo.txt
```

Find installed paths:

```sh
$ wmic qfe get Caption,Description,HotFixID,InstalledOn
```

## Comprehensive talbes of vulnerabilities below:

eDB   Vuln Name         MS#     2K       XP     2003    2008      Vista      7
271   Lsasrv.dll     MS04-011  SP2,3,4  SP0,1    -       -        -         -
350   Util Manager   MS04-019  SP2,3,4  -        -       -        -         -
351   POSIX          MS04-020  SP4      -        -       -        -         -
352   Univ lang. UtilMS04-019   -       SP2,3,4  -       -        -         -
355   Univ lang. UtilMS04-019   -       SP2,3,4  -       -        -         -
1149  PnP Service    MS05-039  P4       SP2      SP1     -        -         -
1197  keybd_event    -         all      all      all     -        -         -
1198  CSRSS          MS05-018  SP3,4    SP1,2    -       -        -         -
1407  Kernel APC     MS05-055  SP4      -        -       -        -         -
1911  Mrxsmb.sys     MS06-030  all      SP2      -       -        -         -
2412  Windows Kernel MS06-049  SP4      -        -       -        -         -
3220  Print spool    -         -        All      -       -        -         -
5518  win32k.sys     MS08-025  SP4      SP2      SP1,2   SP0      SP0,1       -
6705  Churrasco      MS09-012  -        -        All     -        -         -
6705  Churraskito    -         -        All      All     -        -         -
21923 Winlogon       -         All      All      -       -        -         -
11199 KiTrap0D       MS10-015  All      All      All     All      All       All
14610 Chimichurri    MS10-059  -        -        -       All      All       SP0
15589 Task Scheduler MS10-092  -        -        -       SP0,1,2  SP1,2     SP0
18176 AFD.Sys        MS11-080  -        SP3      SP3     -        -         -
100   RPC DCOM       MS03-026  SP3,4    -        -       -        -         -
103   RPC2           MS03-039  all (CN) -        -       -        -         -
109   RPC2           MS03-039  all      -        -       -        -         -
119   Netapi         MS03-049  SP4      -        -       -        -         -
3022  ASN.1          MS04-007  SP2,3,4  SP0,1    -       -        -         -
275   SSL BOF        MS04-011  SP4      ?        -       -        -         -
295   Lsasarv.dll    MS04-011  SP2,3,4  SP0,1    -       -        -         -
734   NetDDE BOF     MS04-031  SP2,3,4  SP0,1    -       -        -         -
1075  Messaging QueueMS05-017  SP3,4    SP0,1    -       -        -         -
1149  PnP Service    MS05-039  SP4      -        -       -        -         -
2223  CP             MS06-040  -        SP1      -       -        -         -
2265  NetIPSRemote   MS06-040  SP0-4    SP0,1    -       -        -         -
2789  NetPManageIP   MS06-070  SP4      -        -       -        -         -
7104  Service exec   MS08-067  SP4      SP2,3    SP1,2   SP0      SP0,1     -
7132  Service exec   MS08-067  SP4      -        SP2     -        -         -
14674 SRV2.SYS SMB   MS09-050  -       -         -       -        SP1,2     -

   MS*           HotFix                         OS
MS16-032     KB3143141    Windows Server 2008 ,7,8,10 Windows Server 2012
MS16-016        KB3136041    Windows Server 2008, Vista, 7 WebDAV
MS15-051     KB3057191     Windows Server 2003, Windows Server 2008, Windows 7, Windows 8, Windows 2012
MS14-058     KB3000061    Windows Server 2003, Windows Server 2008, Windows Server 2012, 7, 8 Win32k.sys
MS14-040     KB2975684     Windows Server 2003, Windows Server 2008, 7, 8, Windows Server 2012
MS14-002     KB2914368     Windows XP, Windows Server 2003
MS13-005     KB2778930    Windows Server 2003, Windows Server 2008, 7, 8,
MS10-092     KB2305420     Windows Server 2008, 7
MS10-015     KB977165     Windows Server 2003, Windows Server 2008, 7, XP
MS14-002     KB2914368    Windows Server 2003, XP
MS15-061     KB3057839    Windows Server 2003, Windows Server 2008, 7, 8, Windows Server 2012
MS11-080     KB2592799    Windows Server 2003, XP
MS11-062     KB2566454    Windows Server 2003, XP
MS15-076     KB3067505    Windows Server 2003, Windows Server 2008, 7, 8, Windows Server 2012
MS16-075     KB3164038    Windows Server 2003, Windows Server 2008, 7, 8, Windows Server 2012
MS15-010     KB3036220    Windows Server 2003, Windows Server 2008, 7, XP
MS11-046     KB2503665    Windows Server 2003, Windows Server 2008, 7, XP

MS11-011 (KB2393802)
MS10-059 (KB982799)
MS10-021 (KB979683)
MS11-080 (KB2592799)

## Exploits worth looking at: MS11-046

https://github.com/SecWiki/windows-kernel-exploits