#!/bin/bash

db="urlmonster"
table="users"
user="root"
pass=$(cat secrets.txt)

mysql -u$user -p$pass -e "create database if not exists $db"
mysql -u$user -p$pass -D$db -e "use $db; create table if not exists links (hashid varchar(6), longurl varchar(50), shorturl varchar(50), primary key(hashid));"
mysql -u$user -p$pass -D$db -e "use $db; insert into links (hashid, longurl, shorturl) values (\"123456\", \"www.google.com\", \"http://localhost/123456\"), (\"098765\", \"www.bing.com\", \"http://localhost/098765\");"
