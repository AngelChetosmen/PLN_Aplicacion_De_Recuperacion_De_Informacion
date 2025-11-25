# app/backend/app.py

import os
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import flask

# Inicializa el servidor Flask
server = flask.Flask(__name__)

# Inicializa la aplicación Dash
app = Dash(
    __name__,
    server=server,
    use_pages=True,  # Activa la funcionalidad de multi-páginas
    pages_folder='dash_pages',  # Carpeta donde vivirán las páginas
    assets_folder='assets', # Aseguramos que Dash sepa dónde está la carpeta
    external_stylesheets=[dbc.themes.BOOTSTRAP], # Tema de Bootstrap
    suppress_callback_exceptions=True # Necesario para callbacks en layouts dinámicos
)

# Define la barra de navegación
navbar = dbc.NavbarSimple(
    children=[
        # Reemplazamos dbc.NavLink por dcc.Link para FORZAR el enrutamiento del lado del cliente
        # y evitar que la página se recargue.
        dbc.NavItem(
            dcc.Link(
                "Procesamiento",
                href="/procesamiento",
                className="nav-link text-light"  # Clases de Bootstrap para que se vea bien
            )
        ),
        dbc.NavItem(
            dcc.Link(
                "Similitud Coseno",
                href="/similitud-coseno",
                className="nav-link text-light"
            )
        ),
        dbc.NavItem(
            dcc.Link(
                "Análisis BERT",
                href="/analisis-bert",
                className="nav-link text-light"
            )
        ),
        # dbc.NavItem(
        #     dcc.Link(
        #         "Resultados",
        #         href="/resultados",
        #         className="nav-link text-light"
        #     )
        # ),
    ],
    brand=[
        html.Img(
            src=app.get_asset_url('image.png'),   
            height="30px",                       
            className="me-2"                     
        ),
        "Recuperación de Información de Poemas |",
        html.Img(
            src=app.get_asset_url('escom.png'),  
            height="30px",                        
            className="ms-2"
        ),
    ],
    brand_href="/", 
    color="primary",
    dark=True,
    className="mb-2"
)

# Layout principal de la aplicación
app.layout = dbc.Container([
    # Almacenes de datos para compartir resultados entre páginas
    # storage_type='session' se borra cuando el usuario cierra la pestaña
    dcc.Store(id='store-cosine-results', storage_type='local'),
    dcc.Store(id='store-bert-results', storage_type='local'),

    navbar,  # La barra de navegación

    dash.page_container  # El contenido de la página actual se renderizará aquí
], fluid=True)

# Punto de entrada para ejecutar el servidor
# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, port=port)