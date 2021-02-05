#!/bin/bash

db="urlmonster"
table="users"
user="root"
pass=$(cat ./secrets.txt)

SECURE_MYSQL=$(expect -c "
set timeout 3
spawn mysql_secure_installation
expect \"Enter current password for root (enter for none):\"
send \"\r\"
expect \"root password?\"
send \"y\r\"
expect \"New password:\"
send \"$pass\r\"
expect \"Re-enter new password:\"
send \"$pass\r\"
expect \"Remove anonymous users?\"
send \"y\r\"
expect \"Disallow root login remotely?\"
send \"y\r\"
expect \"Remove test database and access to it?\"
send \"y\r\"
expect \"Reload privilege tables now?\"
send \"y\r\"
expect eof
")

#
# Execution mysql_secure_installation
#
echo "${SECURE_MYSQL}"

mysql -u$user -p$pass -e "create database if not exists $db"
mysql -u$user -p$pass -D$db -e "use $db; create table if not exists links (hashid varchar(6), longurl varchar(50), shorturl varchar(50), primary key(hashid));"
# mysql -u$user -p$pass -D$db -e "use $db; insert into links (hashid, longurl, shorturl) values (\"123456\", \"www.google.com\", \"http://localhost/123456\"), (\"098765\", \"www.bing.com\", \"http://localhost/098765\");"
