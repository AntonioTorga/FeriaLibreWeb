# tarea3webdev
Tarea 3 Antonio Torga Mellado: La tarea está estructurada en diferentes carpetas para mantener el orden, estan los archivos estaticos y la carpeta donde se almacenaran las imagenes subidas al servidor. Desde mi computador la aplicación corre haciendo python -m flask run (--debug opcionalmente) al parecer por un problema del path de python, pero en otro computador debería correr normalmente desde la carpeta principal. La aplicación utiliza templates, la base de datos, validaciones de front-end y back-end, entre muchas otras cosas. Módulos requeridos serían re, pymysql, hashlib, filetype, werkzeug y bleach.
El mapa y los gráficos funcionan consultando la base de datos y se generan en el front-end mediante leaflet y highcharts.
La base de datos se conecta con el usuario y contraseña de la tarea 2.
Para correr el programa usando un venv nuevo seguir las siguientes instrucciones:
1. Crear venv y activarlo. 
2. Instalar flask, pymysql, filetype, flask_cors, cryptography.
3. Crear la estructura de la base de datos "tarea2" con tarea2.sql, y poblar las tablas región y comuna con region-comuna.sql.
4. Crear si no esta creado el usuario con las credenciales:
 usuario :"cc5002",
 contraseña "programacionweb",
 host: "localhost"
Así debería estar todo listo y funcionando, si recien inicializo la base de datos no habrán datos en esta. 
