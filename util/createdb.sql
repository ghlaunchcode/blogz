CREATE SCHEMA `blogz` DEFAULT CHARACTER SET utf8 ;
CREATE USER 'blogz'@'localhost' IDENTIFIED BY 'blogz';
GRANT ALL ON blogz.* TO 'blogz'@'localhost';