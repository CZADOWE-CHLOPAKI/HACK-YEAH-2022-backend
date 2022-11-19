source .env
mkdir -p mysql_data

docker-compose up -d

sleep 10

docker exec mysql_dev mysql -hlocalhost -uroot -proot -e "CREATE USER IF NOT EXISTS 'sendhybrid'@'localhost' IDENTIFIED BY 'sendhybrid'"

docker exec mysql_dev mysql -hlocalhost -uroot -proot -e "CREATE DATABASE IF NOT EXISTS sendhybrid CHARACTER SET utf8 COLLATE utf8_general_ci"
docker exec mysql_dev mysql -hlocalhost -uroot -proot -e "GRANT ALL PRIVILEGES ON sendhybrid.* TO 'sendhybrid'@'localhost'"
docker exec mysql_dev mysql -hlocalhost -uroot -proot -e "FLUSH PRIVILEGES"
