# Practica3

## Contenido
- [Objetivo de la practica](#objetivo-de-la-practica)
- [Enunciado](#enunciado)
- [Requisitos](#requisitos)
    - [Entorno Virtual](#entorno-virtual)
    - [Dependencias](#dependencias)
    - [Certificado SSL](#certificado-ssl)
    - [Añadir dominio a tu sistema](#añadir-dominio-al-sistema)
- [Ejecución del servidor](#ejecución-del-servidor)
- [Test](#testing)
- [Aspectos adicionles de la práctica](#aspectos-adicionles-de-la-práctica)
    - [Registro de usuarios](#registro-de-usuarios)
    - [Establecer el límite de tamaño de la base de datos](#establecer-el-límite-de-tamaño-de-la-base-de-datos)
    - [Limitar el número de peticiones por usuario u IP](#limitar-el-número-de-peticiones-por-usuario-u-ip)

## Objetivo de la practica
Los objetivos de esta práctica son los siguientes:
- Conocer e implementar una API RESTful sencilla.
- Implementar mecanismos de identificación y autenticación de usuarios.
- Implementar mecanismos de confidencialidad utilizando HTTPS.

## Enunciado 
Vamos a crear un prototipo de base de datos como servicio. Empezaremos con algo totalmente funcional y que se puede utilizar para almacenar documentos en formato JSON. La base de datos se podrá utilizar como una API RESTful y permitirá diferentes cuentas de usuarios.

Para este prototipo, el programa servidor se asumirá en el endpoint
https://myserver.local:5000 donde myserver.local resolverá a 127.0.0.1. 

El servidor se ejecutará en el puerto 5000 y se utilizará el protocolo HTTPS

Aún asi se puede llamar las reglas de forma individual por si algu paso ya esta instalado.
## Requisitos
### Entorno virtual
Para instalar probar el programa es aconsejable crear un entorno virtual y dejar los paquetes instalados en él.

```bash
    python3 -m venv .venv
```
### Dependencias
Una vez se instale el entorno virtual, lo activaremos para que las dependencias se intalen en él. Se necesita ejecutar los siguientes comandos:

```bash
    source ./venv/bin/activate
    make requirements
```
### Certificado SSL
Para poder utilizar HTTPS, es necesario disponer de un certificado y una clave, para ello, crearemos un par de certificados autofirmados con el siguiente comando:

```bash
    make cert
```
Importante que a a la hora de crear el certificado se le ponga el nombre de dominio que se va a utilizar, en este caso myserver.local y de la contraseña que se le ponga a la clave, ya que se va a utilizar en el servidor para iniciarlo.

En caso que haya algun problema exportando el certificado, se le puede indicar a curlo mediante la opción --cacert el certificado que se ha generado.
```bash
    curl --cacert cert/cert.pem https://myserver.local:5000/version
```


### Añadir dominio al sistema
Para poder resolver el dominio myserver.local, es necesario añadir una entrada en el fichero /etc/hosts. Para ello, puedes añadirlo automaticamente con el siguiente comando:

```bash
    make add-domain
```

## Ejecución del servidor
Para ejecutar el servidor, se puede utilizar el siguiente comando:

```bash
    make run
```
Si obtienes el error `Name or service not found` es por que no has añadido el dominio especificado en el apartado [anterior](#añadir-dominio-al-sistema), compruebalo o bien el archivo `/etc/hosts`.
## Testing
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












    
