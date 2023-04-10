# Tópicos Especiales en Telemática | Proyecto 1  B| MOM

## Integrantes

* Alejandro McEwen Cock
* Julian David Bueno Londoño
* Juan Manuel Muñoz Arias

# 1. Introducción

En el marco del curso Tópicos Especiales en Telemática, nos proponemos implementar un Message-Oriented Middleware (MOM) con el objetivo de aplicar los conceptos, vistos en clase, de escalabilidad, tolerancia a fallos y replicación en el diseño y desarrollo del sistema. Este proyecto se inspira en el conocido sistema RabbitMQ, que es ampliamente utilizado en la industria para facilitar la comunicación entre distintas aplicaciones mediante el intercambio de mensajes.

A lo largo de este documento, presentaremos la arquitectura del sistema distribuido propuesto, el diagrama de clases, los requisitos del sistema y las instrucciones para ejecutarlo.

# 2. Arquitectura del MOM

<p align="center">
  <img src="https://user-images.githubusercontent.com/28406146/230799407-4033c08b-fac8-4120-8366-0238cfd036ed.png">
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

* La conexión y desconexión al sistema requieren la autenticación de los usuarios, lo que garantiza que solo los usuarios autorizados puedan acceder a los servicios.

* Los usuarios solo pueden eliminar canales o colas que hayan creado. Al eliminar una cola, si aún quedan mensajes pendientes de envío, no se podrá realizar la eliminación hasta que todos los mensajes hayan sido procesados.

* El envío y recepción de mensajes dentro del sistema identifica a los usuarios involucrados, lo que permite un mejor seguimiento y control de las comunicaciones.

* Todos los servicios mencionados se exponen a través de una API REST para facilitar la interacción con los clientes.

* El MOM implementa un sistema de replicación de tipo líder-seguidor (leader-follower), lo que permite una distribución eficiente de las tareas y garantiza la coherencia de los datos entre las diferentes instancias.

* El sistema cuenta con múltiples instancias del MOM, lo que proporciona tolerancia a fallos. En caso de que una instancia falle, las otras pueden continuar ejecutando el trabajo sin interrupciones.

* El MOM permite conectar múltiples instancias, lo que aumenta su capacidad para manejar cargas de trabajo más elevadas y crecer en función de las demandas del sistema.

* La escalabilidad del MOM se logra mediante la utilización de una estrategia de distribución de carga Round Robin, que distribuye las solicitudes entrantes de manera equitativa entre las instancias disponibles.
