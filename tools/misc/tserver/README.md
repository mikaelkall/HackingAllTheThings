# Tserver

## Summary

In some situations you may want to expose a port from your target machine and tunnel it back to your attacker machine
this is because the port may be blocked by a firewall or listen on localhost interface only.
If you have SSH access it is easy as you can create an SSH tunnel. In situations when you don't have SSH access to
the machine you can setup SSH on your own machine on port 80 and instead tunnel back the port to it with use the '-R' flag.
Problem with that is that you expose SSH to a hostile environment and also you need to reconfigure SSH.
This application and docker container solves this problem by setup a SSH server that only allow SSH tunnel.
Also as the container use --net=host you have access to your network namespace but protect yourself from that someone
ssh into your SSH server to abuse it.


## Tserver

Simple run these commands to build and start docker container.

```sh
    ./tserver.sh build
    ./tserver.sh up
```

You can run the docker logs command to check what password is set on the contaier.
Note as /bin/true is set as shell on the root container only ssh tunnel is possible with this container.
Also as --net=host is used it has access to the same network namespace as your host os.

```
⬢  tserver  docker logs tserver
chpasswd: password for 'root' changed
ROOT PW: xxxxxxxxxxxxxxxxxxxxxxxxx
Server listening on 0.0.0.0 port 80.
Server listening on :: port 80.

```


## Tclient

