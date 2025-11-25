# wsgi.py

# Importa el servidor Flask que se ha inicializado dentro de tu aplicación Dash.
# La ruta es: carpeta_app.carpeta_backend.archivo_app:variable_servidor

from app.backend.app import server as application

# Gunicorn buscará la variable 'application' por defecto.
# 'application' ahora contiene la instancia del servidor Flask de Dash.
# Si prefieres usar 'server' en el Procfile/manifest.yml, puedes renombrarla:
# server = application