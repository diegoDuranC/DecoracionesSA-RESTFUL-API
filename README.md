# FLASK | RESTful API DecoracionesSA

## INSTALACIÓN
Se debe instalar python, para evitar posibles incompatibilidades, esta api se desarrolló con Python 3.11.3
### Creación Entontorno Virutal Python
Generalmente se recomienda trabajar con 'virtual environments' en python, **AFUERA DE LA CARPETA CONTENEDORA DEL PROYECTO**, para crearlo ejecutar:

```
    python -m venv "nombre_del_entorno_virtual"
```
Una vez creado, activar el entorno virtual (si se encuentra en la misma dirección de la carpeta del entorno)
```
    .\nombre_del_entorno_virtual\Scripts\activate
```
Instalar los paquetes necesarios con el archivo requirements.txt

```
    pip install -r requirements.txt
```
## CONFIGURACIÓN
### Crear un archivo de configuración
En la carpeta raíz crear un archivo .env con el nombre config.env con los siguientes campos:

- **DB_USER**="Usuario de postgres"
- **DB_PASSWORD**="Contraseña"
- **DB_HOST**="Host"
- **DB_PORT**="Puerto Base de Datos"
- **DB_NAME**="Nombre de la Base de Datos"

## INICIAR LA APLICACIÓN
Para iniciar la aplicación ejecutar el siguiente comando:

```
    python main.py
```
