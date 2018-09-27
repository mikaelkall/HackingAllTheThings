# Fuzzing

Example on fuzzing get parameters

```sh
wfuzz -c -w /usr/share/wordlist/SecLists/Discovery/Web_Content/burp-parameter-names.txt --hh 19 -u http://10.10.10.69/sync?FUZZ=yesterday
```

Example on fuzz username in a web application.

```sh
wfuzz -c -z file,names.txt --hw 657 -d "username=FUZZ&password=password" http://10.10.10.73/login.php
```


```sh
wfuzz -c --hl=2 -z range,1-65535 http://10.10.10.55:60000/url.php\?path\=http://localhost:FUZZ
```
