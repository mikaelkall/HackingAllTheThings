# socat[tricks]

## Run command as a service
 
$ socat TCP-LISTEN:6666,fork,reuseaddr exec:/command
 
## Forward port to a different port.
 
socat TCP-LISTEN:9999,reuseaddr,fork,su=nobody TCP:nighter.se:80
 
socat TCP-LISTEN:80,fork TCP:\<address\>:80
