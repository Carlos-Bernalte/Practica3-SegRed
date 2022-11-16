# Practica3
Los objetivos de esta práctica son los siguientes:
- Conocer e implementar una API RESTful sencilla.
- Implementar mecanismos de identificación y autenticación de usuarios.
- Implementar mecanismos de confidencialidad utilizando HTTPS.
## Enunciado
Vamos a crear un prototipo de base de datos como servicio. Empezaremos con
algo totalmente funcional y que se puede utilizar para almacenar documentos
en formato JSON. La base de datos se podrá utilizar como una API RESTful y
permitirá diferentes cuentas de usuarios.

Para este prototipo, el programa servidor se asumirá en el endpoint
https://myserver.local:5000 donde myserver.local resolverá a 127.0.0.1. 

## Entorno virtual y dependencias
Para instalar probar el programa es aconsejable crear un entorno virtual y dejar los paquetes instalados en él. Para ello, se puede utilizar el siguiente:


```bash
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
```
Una vez activado el entorno virtual, se pueden instalar los paquetes necesarios con el siguiente comando:

```bash
    pip install -r requirements.txt
```
## Certificados
Para poder utilizar HTTPS, es necesario disponer de un certificado y una clave, para ello, crearemos un par de certificados autofirmados con el siguiente comando:

```bash
    mkdir cert
    openssl req -x509 --newkey rsa:4096 --out cert/cert.pem --keyout cert/key.pem --days 365
```
Para que curl pueda utilizar el certificado, es necesario indicarle la ruta al certificado con el parámetro --cacert. Para ello, se puede utilizar el siguiente comando:

```bash
    curl --cacert cert/cert.pem https://myserver.local:5000
```
O bien puedes añadir el certificado a tu sistema operativo para que curl por defecto busque ahí. En Linux, puedes añadir el certificado a la lista de certificados de confianza con el siguiente comando:

```bash
    sudo cp cert/cert.pem /usr/local/share/ca-certificates/
    sudo update-ca-certificates
```
## Resolver el dominio del servidor
Para poder utilizar el dominio myserver.local, es necesario añadir una entrada en el fichero /etc/hosts. Para ello, puedes añadirlo automaticamente con el siguiente comando:

```bash
    sudo sh -c "echo '127.0.0.1 myserver.local' >> /etc/hosts" 
```

## Ejecución del servidor
Para ejecutar el servidor, se puede utilizar el siguiente comando:

```bash
    python -m src.run
```
## Ejecución de los tests
Como tal no hay tests, pero se puede probar el funcionamiento del servidor con el siguiente comando llenando la base de datos con datos de prueba:

```bash
    python test_db.py
```




    
