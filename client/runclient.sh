docker build -t my-apache2 .
docker run -dit --name client-TET -p 8080:80 my-apache2