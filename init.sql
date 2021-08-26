use mysql;
CREATE DATABASE IF NOT EXISTS `shoreapp`;
CREATE DATABASE IF NOT EXISTS `shoreapp_test`;
CREATE USER 'shore'@'%' IDENTIFIED BY 'qwe90qwe';
GRANT ALL ON *.* TO 'shore'@'%';
flush privileges;
