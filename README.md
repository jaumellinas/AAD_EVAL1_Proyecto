# AAD_EVAL1_Proyecto

**Conector MariaDB**  
Acceso a Datos — 2º DAM  
Jaume Llinàs Sansó

## Estructura del proyecto

```
AAD_EVAL1_Proyecto/
├── conectorMariaDB/
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── dashboard/
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/
│   │   └── dashboard/
│   │       └── index.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── visor/
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/
│   │   └── visor/
│   │       └── index.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── README.md
├── __init__.py
└── manage.py
```

## Descripción general

Este proyecto consiste en conseguir que una aplicación creada por nosotros se a una base de datos MariaDB y manejar dichos datos. En nuestro caso hemos creado dos apps: **un dashboard** y **un visor de tablas en HTML**.

En el **dashboard**, se definen consultas en el backend que luego son plasmadas en el frontend en forma de entero o de gráfico. En nuestro caso, hay consultas que sólo retornan un valor (como en el caso del número de clientes o de películas) o que retornan varios (que son procesados como gráficos gracias a Chart.js).

En cambio, en el **visor de tablas** se itera sobre todas las tablas de una base de datos y sobre todas las columnas y filas de dichas tablas. Con esto conseguimos mostrar toda la información de todas las tablas de una base de datos concreta sin tener que tocar el código cada vez que la BBDD cambia.

Para ambas apps se usa una base de datos de muestra llamada [sakila](https://dev.mysql.com/doc/sakila/en/). No obstante, el código del visor de tablas es reutilizable para otras bases de datos. Lo único que hará falta es modificar los valores de conexión a la base de datos del archivo `.env`.

> [!NOTE]  
> Nuestras apps están escritas en **Django**, un framework de **Python**.

## Requisitos
* Python 3.12+
  * Django
  * Librería de MariaDB
  * loadenv
  * Gunicorn (sólo en despliegue cloud)

> [!IMPORTANT]  
> Esta guía de instalación asume que el usuario **ya dispone de una base de datos a la que conectarse**. Por tanto, toda la parte de instalación de MariaDB y el volcado de las bases de datos al programa es omitida.

## Variables .env
* MARIADB_USER
* MARIADB_PASSWORD
* MARIADB_HOST
* MARIADB_PORT
* MARIADB_DATABASE
* DJANGO_SECRET_KEY

## Despliegue en local
Para documentar el despliegue de nuestras apps, asumiremos que el usuario no tiene ninguno de nuestros requisitos instalados. 

El proceso para llevar a cabo el despliegue en local consiste en: 
1. Instalar la última versión de [Python](https://www.python.org/downloads/).
2. Instalar el [conector para C de MariaDB](https://mariadb.com/docs/connectors/mariadb-connector-c/mariadb-connector-c-guide).
3. Clonamos nuestro proyecto de GitHub en la máquina.
4. Abrimos una terminal y navegamos hasta el directorio donde se encuentra nuestra app. 
5. En dicho directorio, creamos un `venv` y lo activamos.
6. Instalamos los requisitos con `pip install -r requirements.txt`
7. Rellenamos el archivo .env del proyecto con las variables necesarias.
8. Ejecutamos el comando `python manage.py runserver`.

## Despliegue a entorno cloud
De forma extra y siendo realizada esta parte tras haber acabado la actividad en sí, he intentado desplegar esta misma aplicación en algún servicio “serverless” como Vercel o Heroku. No obstante, el módulo `mariadb` de Python suele dar problemas con este tipo de servicios al depender del módulo escrito en C de MariaDB. Por tanto, al no tener la posibilidad de poder instalar módulos en las máquinas que corren nuestro servicio, he tenido que optar por otra solución.

Para no tener que reeditar el código ni tener que usar módulos como `SQLAlchemy`, he optado por desplegar mi aplicación en una máquina virtual de Azure, usando los créditos gratuitos que nos proporciona Sant Josep.

El proceso para llevar a cabo el despliegue es muy sencillo: 
1. Creamos la máquina virtual y nos conectamos a ella por SSH.
2. Clonamos nuestro proyecto de GitHub en la máquina.
3. Instalamos `python` y `libmariadb-dev` con `apt`.
4. Abrimos el directorio donde se encuentra nuestra app, creamos un `venv` y lo activamos.
5. Instalamos los requisitos con `pip install -r requirements.txt`
6. (Sólo para cloud) Instalamos `gunicorn` (servidor web más robusto) con `pip install gunicorn`.
7. Rellenamos el archivo .env del proyecto con las variables necesarias.
8. Ejecutamos `gunicorn` con el comando de abajo.

```
sudo $(pwd)/.venv/bin/gunicorn conectorMariaDB.wsgi:application \
  --bind 0.0.0.0:80 \
```

Con este comando gunicorn empezará a servir nuestra app a través del puerto 80 de nuestra máquina virtual. Es importante recordar abrir el puerto correspondiente en la consola de administración de Azure.

En mi caso, al querer servir la aplicación a través de HTTPS, ejecutaré el mismo comando de antes cambiando el puerto 80 por el 443 y haciendo referencia a los certificados SSL que usará mi máquina virtual para cifrar el tráfico. 

```
sudo $(pwd)/.venv/bin/gunicorn conectorMariaDB.wsgi:application \
  --bind 0.0.0.0:443 \
  --certfile=/etc/ssl/cloudflare/origin.pem \
  --keyfile=/etc/ssl/cloudflare/origin.key
```

> [!NOTE]  
> El certificado que yo referencio me ha sido generado por Cloudflare siguiendo [este tutorial](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/). Evidentemente, mi certificado está generado por Cloudlare porque es el servicio con el que **yo** gestiono mis dominios. En caso de querer realizar este mismo paso con otro proveedor, muy seguramente los pasos a seguir diferirán de los del tutorial referenciado.

Con Azure conectado a Cloudflare y con los certificados SSL ya generados por este, podremos conectarnos a mi instancia de la aplicación [a través de este enlace](https://aad1.jaume.wtf/).

## Uso de IA y otros recursos
Este proyecto ha sido mayoritariamente elaborado guiándome por posts de foros del estilo StackOverflow, así como guías de Django como la de W3Schools. No obstante, para funciones específicas como la sintaxis de la librería de MariaDB para Python o el afinado de ciertos elementos de CSS con Bulma se ha usado la inteligencia artificial Claude a modo de corrector, pasándole el script entero y comentando (no corrigiendo directamente) las partes que no le gustaban.