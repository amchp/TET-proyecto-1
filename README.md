# Tópicos Especiales en Telemática | Proyecto 1 | MOM

## Integrantes

* Alejandro McEwen Cock
* Julian David Bueno Londoño
* Juan Manuel Muñoz Arias

# 1. Introducción

En el marco del curso Tópicos Especiales en Telemática, nos proponemos implementar un Message-Oriented Middleware (MOM) con el objetivo de aplicar los conceptos, vistos en clase, de escalabilidad, tolerancia a fallos y replicación en el diseño y desarrollo del sistema. Este proyecto se inspira en el conocido sistema RabbitMQ, que es ampliamente utilizado en la industria para facilitar la comunicación entre distintas aplicaciones mediante el intercambio de mensajes.

A lo largo de este documento, presentaremos la arquitectura del sistema distribuido propuesto, el diagrama de clases, los requisitos del sistema y las instrucciones para ejecutarlo.

# 2. Arquitectura del MOM


<p align="center">
  <img src="https://user-images.githubusercontent.com/69641274/230806409-4b7e2218-e6ac-441b-a306-e0829fa06275.jpg">
</p>

El sistema distribuido desarrollado es un Message-Oriented Middleware (MOM) construido desde cero utilizando Python 3.8.10. Este middleware permite la comunicación entre diferentes aplicaciones mediante el intercambio de mensajes.

Los siguientes, son los puntos claves de la arquitectura del sistema:

1. Las peticiones de los clientes se realizan a través de HTTP y llegan a un balanceador de carga NGINX, el cual se encuentra dockerizado y se ejecuta en una máquina virtual EC2 de AWS. El balanceador de carga escucha en el puerto 80.

2. El balanceador de carga NGINX se conecta a una o varias instancias de MOM, cada una de ellas ejecutándose en máquinas EC2 distintas. Los MOM también están dockerizados.

3. Cada MOM posee dos servidores: un servidor REST que recibe las solicitudes HTTP de los clientes, como enviar mensajes, registrarse, recibir mensajes, ver tópicos, etc., y un servidor gRPC que se comunica mediante HTTP2. El servidor REST se ejecuta en el puerto 80 y utiliza el framework Bottle de Python, mientras que el servidor gRPC se ejecuta en el puerto 8080 y utiliza la librería gRPC de Google.

4. Los MOM se comunican entre sí a través del servidor gRPC para replicar información y mantenerse actualizados cuando se conectan a la red.

5. El balanceador de carga NGINX se comunica con los MOM mediante HTTP y emplea el algoritmo Round Robin para distribuir las solicitudes entre las distintas instancias de MOM.

6. El sistema utiliza el enfoque de replicación Leader and Followers para la gestión de solicitudes. El líder MOM recibe las solicitudes que implican escritura en disco, como lo pueden ser POST y DELETE, y los seguidores reciben las solicitudes GET. El líder escribe la información en su disco y, posteriormente, la replica a las otras instancias de MOM.

Esta arquitectura distribuida garantiza alta disponibilidad, escalabilidad y tolerancia a fallos, permitiendo el manejo eficiente de mensajes entre aplicaciones.

# 3. Diagrama de clases

<p align="center">
  <img src="https://user-images.githubusercontent.com/28406146/230799410-f6b793cd-2c12-41b0-8cf1-ced4431a184f.png">
</p>

Manejamos tres objetos MOM Topics, Queue, y User. Cada tópico tiene un ID, nombre, unos usuarios subscritos y unas colas para mandarle información a esos usuarios. Cada cola tiene un ID, usuario creador o que manda los mensajes, un usuario que recibe los mensajes, y los mensajes en la cola. Por último usuarios que tienen un ID, nombre, clave, y las colas que son receptores de.

En nuestro sistema gestionamos tres objetos principales: Topics, Queue y User.

* **Topics:** Los tópicos son el núcleo de la organización del contenido en el MOM. Cada tópico tiene un identificador único (ID), un nombre y una lista de usuarios suscritos. Además, los tópicos cuentan con colas asociadas que permiten enviar información a los usuarios suscritos.

* **Queue:** Las colas facilitan el envío de mensajes entre los usuarios. Cada cola posee un ID único, un usuario creador (que envía los mensajes) y un usuario receptor (que recibe los mensajes). También almacenan los mensajes que están en la cola, a la espera de ser entregados al receptor correspondiente.

* **User:** Los usuarios representan a los participantes del sistema MOM. Cada usuario tiene un ID único, un nombre y una clave para la autenticación. Además, los usuarios tienen asociadas las colas en las que actúan como receptores de mensajes.

# 4. Requerimientos de diseño

La implementación del MOM propuesto cuenta con las siguientes características y requisitos, diseñados para garantizar un funcionamiento eficiente y seguro:

| Requerimientos  |
| ------------- |
| La conexión y desconexión al sistema requieren la autenticación de los usuarios, lo que garantiza que solo los usuarios autorizados puedan acceder a los servicios.  |
| Los usuarios solo pueden eliminar canales o colas que hayan creado. Al eliminar una cola, si aún quedan mensajes pendientes de envío, no se podrá realizar la eliminación hasta que todos los mensajes hayan sido procesados.  |
| El envío y recepción de mensajes dentro del sistema identifica a los usuarios involucrados, lo que permite un mejor seguimiento y control de las comunicaciones.  |
| Todos los servicios mencionados se exponen a través de una API REST para facilitar la interacción con los clientes.  |
| El MOM implementa un sistema de replicación de tipo líder-seguidor (leader-follower), lo que permite una distribución eficiente de las tareas y garantiza la coherencia de los datos entre las diferentes instancias.  |
| El sistema cuenta con múltiples instancias del MOM, lo que proporciona tolerancia a fallos. En caso de que una instancia falle, las otras pueden continuar ejecutando el trabajo sin interrupciones.  |
| El MOM permite conectar múltiples instancias, lo que aumenta su capacidad para manejar cargas de trabajo más elevadas y crecer en función de las demandas del sistema.  |
| La escalabilidad del MOM se logra mediante la utilización de una estrategia de distribución de carga Round Robin, que distribuye las solicitudes entrantes de manera equitativa entre las instancias disponibles.  |
| En caso de que una instancia de MOM falle y se desconecte, se ha implementado un sistema de actualización llamado Update para garantizar la consistencia de los datos entre las instancias. Este sistema funciona de la siguiente manera:  |
| En caso de que una instancia de MOM falle y se desconecte, se ha implementado un sistema de actualización llamado Update para garantizar la consistencia de los datos entre las instancias. Este sistema funciona de la siguiente manera:<br><br> • Cuando un MOM se inicia, solicita los archivos log.json de todas las demás instancias activas en la red.<br><br>• El MOM compara los archivos recibidos y selecciona aquel con el registro (log) más extenso, ya que será el más actualizado.<br><br>• A continuación, el MOM compara su propio archivo log.json con el del registro más actualizado. Si ambos archivos son iguales, no será necesario realizar ninguna actualización, ya que la instancia está al día con la información más reciente.<br><br>• Si el registro local es menor que el más actualizado, el MOM tomará todos los archivos JSON de la instancia con la información más reciente. Estos archivos se recibirán a través de gRPC.<br><br>• Una vez recibida la información actualizada, el MOM sobrescribirá sus propios archivos y, posteriormente, iniciará su servidor REST.<br><br> Es importante mencionar que el servidor gRPC se inicia simultáneamente con el sistema de actualización (Update) en hilos separados. Esto se debe a que, durante el proceso de actualización, es posible que se reciban actualizaciones adicionales por replicación, las cuales deben ser gestionadas adecuadamente. De esta manera, el sistema de actualización garantiza la coherencia y consistencia de los datos entre las distintas instancias de MOM, incluso en situaciones en las que una o más instancias fallen o se desconecten temporalmente. |

# 5. Ejecución del sistema

A continuación, se detalla el proceso de instalación del sistema, incluyendo los prerrequisitos y la configuración del servidor NGINX y las instancias de MOM.

## Prerrequisitos

1. Crear una máquina virtual en AWS EC2 y abrir los puertos 80 y 8080 (8080, en caso de que sea una máquina para una instancia MOM) para una para permitir conexiones entrantes desde cualquier dirección IP.

2. Es recomendable asignar una dirección IP elástica a la máquina virtual, lo que evitará la necesidad de reconfigurar las direcciones IP cada vez que la máquina se reinicie.

3. Conéctate a la máquina virtual mediante SSH.

4. Clona el repositorio del proyecto ejecutando el siguiente comando:

```sh
git clone https://github.com/amchp/TET-proyecto-1.git
```

5. Navega al directorio del proyecto:

```sh
cd TET-proyecto-1
```

6. Instala Docker utilizando el archivo dockersetup.sh proporcionado en el repositorio:

```sh
sh dockersetup.sh
```

Con Docker instalado, ahora puedes configurar el servidor NGINX y las instancias de MOM.

## Configuración del servidor NGINX

1. Navega al directorio del balanceador de carga:

```sh
cd loadBalancer
```

2. Edita el archivo nginx.conf para agregar las direcciones IP públicas de las máquinas en las que se ejecutarán las instancias de MOM. Utilizar direcciones IP elásticas es recomendable para evitar reconfiguraciones constantes.

3. Ejecuta el siguiente comando para iniciar el contenedor de Docker:

```sh
docker-compose up
```

4. Si encuentras problemas relacionados con permisos, ejecuta el comando sudo su para obtener privilegios de superusuario y vuelve a intentar ejecutar docker-compose up.

Una vez completados estos pasos, tu balanceador de carga NGINX estará listo para operar, y podrás comenzar a utilizar el sistema MOM con sus funcionalidades completas.

## Configuración de la instancia MOM

1. Navega al directorio del MOM:

```sh
cd MOM
```

2. Edita el archivo config.py para agregar las direcciones IP de las demás instancias de MOM:

```python
import os
BASE_DIR = os.getcwd()
MOM_INSTANCES = ["54.146.228.238:8080", "34.236.17.72:8080"]
SERVER_ADDRESS = "0.0.0.0"
REST_SERVER_PORT = 80
GRPC_SERVER_PORT = 8080
GRPC_TIMEOUT = 2
```

La línea de interés es la que declara las instancias de otros MOM:

```python
MOM_INSTANCES = ["54.146.228.238:8080", "34.236.17.72:8080"]
```

Debes editar este arreglo agregando las direcciones IP públicas (o elásticas) de los demás MOM. No incluyas la dirección IP de la misma máquina. Asegúrate de que las direcciones IP estén acompañadas por ":8080", ya que las conexiones al servidor gRPC utilizan este puerto.

3. Una vez editado el archivo, guarda los cambios y ejecuta los siguientes comandos para construir e iniciar el contenedor de Docker:

```sh
docker-compose build
docker-compose up
```

Con estos pasos completados, tu instancia de MOM estará en funcionamiento y lista para procesar mensajes en el sistema. Ahora puedes aprovechar todas las funcionalidades que ofrece el Message-Oriented Middleware.
