# Tunnel

## SSH tunnel [ Bind local port to remote port ]
// Example is if you need to access a port on your server which can only be accessed from localhost and not remotely.

ssh -nNT -L \<local port\>:localhost:\<remote port\> user@remoteserver.com

## Magic shortcut gives access to tunnel settings when already connected "ssh>" 

alt ~ space + shift+c

-L 8002:xxx.xxx.xxx:80

## Access like this.

```sh
nc localhost -p \<local port\>
```

## sshuttle ( forward everything)

```sh
sshuttle --dns -r <username>@hostname 0.0.0.0/0 
```

# Execute this on remote server to tunnel back 445 to host. ( Note first configure SSH to listen on port 80 on host )

```sh
plink.exe -l root -pw password -R 445:127.0.0.1:445 10.11.0.xxx -P 80 #
```
