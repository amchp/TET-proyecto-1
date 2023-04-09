# TET-proyecto-1

## Arquitectura del MOM

![DIagrama de arquitectura drawio](https://user-images.githubusercontent.com/28406146/230799407-4033c08b-fac8-4120-8366-0238cfd036ed.png)

Tenemos un servidor NGINX que recibe y a un cluster de MOMs que usan la estrategia Leader follower de replicación.

## Diagrama de objetos

![Diagrama de objetos drawio](https://user-images.githubusercontent.com/28406146/230799410-f6b793cd-2c12-41b0-8cf1-ced4431a184f.png)

Manejamos tres objetos MOM Topics, Queue, y User. Cada tópico tiene un ID, nombre, unos usuarios subscritos y unas colas para mandarle información a esos usuarios. Cada cola tiene un ID, usuario creador o que manda los mensajes, un usuario que recibe los mensajes, y los mensajes en la cola. Por último usuarios que tienen un ID, nombre, clave, y las colas que son receptores de.

## Requerimientos de diseño

*La conexión / desconexión, debe ser con usuarios autenticados.
*Solo puede borrar canales o colas de los usuarios que los crearon
  * Si se borra una cola y no se han terminado de mandar los mensajes no se puede borrar
*El envío y recepción de mensajes debe identificar los usuarios.
*Todos estos servicios deben ser expuestos como un API REST hacia los Clientes.
*El MOM tiene un sistema de replicación leader follower.
*El MOM tiene varias instancias para que si una instancia falla las otras puedan hacer el trabajo.
*El MOM se le pueden conectar varias instancias
*EL MOM es escalable porque utiliza una estrategia de distribución de carga round robin.
