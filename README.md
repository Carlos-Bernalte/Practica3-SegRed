# Practica3
Los objetivos de esta práctica son los siguientes:
- Conocer e implementar una API RESTful sencilla.
- Implementar mecanismos de identificación y autenticación de usuarios.
- Implementar mecanismos de confidencialidad utilizando HTTPS.
## Enunciado y requisitos
Vamos a crear un prototipo de base de datos como servicio. Empezaremos con
algo totalmente funcional y que se puede utilizar para almacenar documentos
en formato JSON. La base de datos se podrá utilizar como una API RESTful y
permitirá diferentes cuentas de usuarios.

Para este prototipo, el programa servidor se asumirá en el endpoint
https://myserver.local:5000 donde myserver.local resolverá a 127.0.0.1. 

El servidor se ejecutará en el puerto 5000 y se utilizará el protocolo HTTPS

Toda la instalación de los requisitos que necesitamos para que la practica funcione se pueden realizar con el la orden del Makefile:

```bash
    make install
```
Aún asi se puede llamar las reglas de forma individual por si algu paso ya esta instalado.

### Entorno virtual y dependencias
Para instalar probar el programa es aconsejable crear un entorno virtual y dejar los paquetes instalados en él.


```bash
    make venv
```
Una vez se instale el entorno virtual, se pueden instalar los paquetes necesarios con el siguiente comando:

```bash
    make requirements
```
### Certificados
Para poder utilizar HTTPS, es necesario disponer de un certificado y una clave, para ello, crearemos un par de certificados autofirmados con el siguiente comando:

```bash
    make cert
```
En caso que haya algun problema exportando el certificado, se le puede indicar a curlo mediante la opción --cacert el certificado que se ha generado.
```bash
    curl --cacert cert/cert.pem https://myserver.local:5000/version
```


### Resolver el dominio del servidor
Para poder utilizar el dominio myserver.local, es necesario añadir una entrada en el fichero /etc/hosts. Para ello, puedes añadirlo automaticamente con el siguiente comando:

```bash
    make add-domain
```

## Ejecución del servidor
Para ejecutar el servidor, se puede utilizar el siguiente comando:

```bash
    make run
```
## Ejecución de los tests
Como tal no hay tests, pero se puede probar el funcionamiento del servidor con el siguiente comando llenando la base de datos con datos de prueba:

```bash
    make test
```
En el codigo se puede apreciar una linea donde desabilitamos los warnings de certificado, esto es debido a que el certificado es autofirmado y no es seguro, pero para este caso es suficiente. [Link del debate](https://github.com/urllib3/urllib3/issues/497).

```python
    import urllib3
    urllib3.disable_warnings()
```

## Aspectos adicionles de la práctica
### Registro de usuarios
Se ha tenido en cuenta que tanto `username` como `password` no puedan ser vacios, y que el `username` no pueda tener espacios en blanco para evitar problemas de identificación.

### Establecer el límite de tamaño de la base de datos
Para evitar el uso excesivo de memoria, se podría establecer un limite de tamaño de la base de datos o un limite de tamaño de cada documento. Y en caso de que se supere el limite, se podria eliminar el documento mas antiguo o enviar algun mensaje de error.

### Limitar el número de peticiones por usuario u IP
Para evitar el uso excesivo de recursos, se podría establecer un limite de peticiones por usuario o por IP. Y en caso de que se supere el limite, se podria bloquear el usuario o la IP.

Authors
    :  [Carlos Bernalte García-Junco](https://github.com/Carlos-Bernalte)
    :  [Angel García Collado](https://github.com/theangelogarci)












    
