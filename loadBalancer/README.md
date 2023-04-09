# NGINX

## Installar docker

Ir a la carpeta de atras, y corres el dockersetup.sh

```
chmod +x dockersetup.sh
./dockersetup.sh
```

## Cambiar configuración de nginx

Cambia la configuración del nginx.conf para que en los upstream groups para que las ips de la servers sean correctas.

## Correr docker

Ya solo hay que correr el docker compose

```
sudo docker compose build
sudo docker compose up -d
```

y debería funcionar el nginx.