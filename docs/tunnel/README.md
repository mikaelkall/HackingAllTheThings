# Tunnel

## SSH tunnel [ Bind local port to remote port ]
// Example is if you need to access a port on your server which can only be accessed from localhost and not remotely.

ssh -nNT -L \<local port\>:localhost:\<remote port\> user@remoteserver.com

## Magic shortcut gives access to tunnel settings when already connected "ssh>" 

alt ~ space + shift+c

-L 8002:xxx.xxx.xxx:80

## Access like this.

nc localhost -p \<local port\>


## sshuttle ( forward everything)

 ```sh
sshuttle --dns -r <username>@hostname 0.0.0.0/0 
 ```
