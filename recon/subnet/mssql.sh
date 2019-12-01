#!/bin/bash
nmap -p 1433 --script ms-sql-info --script-args mssql.instance-port=1433 10.11.1.0/24
