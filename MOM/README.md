# MOM

## Installar docker

Ir a la carpeta de atras, y corres el dockersetup.sh

```
chmod +x dockersetup.sh
./dockersetup.sh
```

## Cambiar configuración del MOM

Cambia la configuración del config.py para que tenga las IPS de los otros MOM. Las IPS deberían tener el puerto de gRPC.

## Correr docker

Ya solo hay que correr el docker compose

```
sudo docker compose build
sudo docker compose up -d
```

y debería funcionar el nginx.