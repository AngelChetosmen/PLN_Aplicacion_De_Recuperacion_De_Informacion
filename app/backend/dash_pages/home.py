# app/backend/dash_pages/home.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Registra esta página como la página de inicio (ruta /)
dash.register_page(__name__, path='/', name='Inicio')

# Contenido de la página de inicio, basado en tu PDF
layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H1(
                        "Proyecto: Recuperación de Información en Poemas", 
                        className="text-primary"
                    ),
                    html.H4("Instituto Politécnico Nacional - ESCOM"),
                    html.P(
                        "Presentado por: Angel Vega",
                        className="text-muted"
                    ),
                ])
            ], className="shadow-sm mb-4"),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Objetivo del Proyecto", className="mt-4"),
            dbc.Alert(
                [
                    html.H5("Solución Propuesta", className="alert-heading"),
                    html.P(
                        "Desarrollar una herramienta que analice poemas en lenguaje español "
                        "mediante técnicas de recuperación de información."
                    )
                ],
                color="primary"
            ),
            
            html.P(
                "El uso del Procesamiento de Lenguaje Natural (PLN) ha revolucionado la forma en que "
                "interactuamos con la información textual."
            ),
            html.P(
                "Este proyecto aplica el método de recuperación de información a poemas literarios "
                "en español, un recurso extenso e interesante que abarca diversas etapas literarias."
            ),
            
            html.H3("Funcionamiento Esperado", className="mt-3"),
            html.P(
                "La herramienta permite al usuario ingresar un poema de prueba. El sistema lo "
                "analiza y devuelve los 10 poemas más similares que se encuentran dentro "
                "de un corpus."
            ),
            html.P(
                "Además, el sistema obtiene el contexto entre los poemas similares y "
                "determina un posible género literario basándose en bancos de palabras clave."
            ),

        ], width=12)
    ]),
    
    html.Hr(className="my-4"),

    dbc.Row([
        dbc.Col([
            html.H2("Metodología Aplicada", className="mb-3"),
            html.P(
                "Para lograr la recuperación de información, se implementaron dos "
                "enfoques principales:"
            ),
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col(md=6, children=[
            dbc.Card([
                dbc.CardHeader(html.H4("1. Similitud Coseno (TF-IDF)")),
                dbc.CardBody([
                    html.P(
                        "El primer método es el enfoque clásico. Primero, se realiza un "
                        "procesamiento de texto que incluye:"
                    ),
                    html.Ul([
                        html.Li("Tokenization"),
                        html.Li("Eliminación de Stopwords"),
                        html.Li("Lemmatization")
                    ]),
                    html.P(
                        "Luego, se genera un corpus normalizado y se emplea la "
                        "similitud coseno para encontrar poemas similares, "
                        "permitiendo análisis por Unigramas y Bigramas."
                    ),
                    dbc.Alert(
                        "Resultado: Este método arrojó similitudes bajas, "
                        "generalmente menores al 13%.",
                        color="warning",
                        className="mt-3"
                    )
                ])
            ], className="h-100 shadow-sm")
        ]),

        dbc.Col(md=6, children=[
            dbc.Card([
                dbc.CardHeader(html.H4("2. Sentence Transformer (BERT)")),
                dbc.CardBody([
                    html.P(
                        "El segundo método utiliza un modelo de Lenguaje (LM) moderno "
                        "tipo BERT para generar 'Embeddings' (vectores numéricos) "
                        "de los poemas."
                    ),
                    html.P(
                        "Estos vectores capturan el significado y contexto del texto de "
                        "una forma mucho más profunda. Al comparar estos embeddings, "
                        "se obtiene una similitud mejorada."
                    ),
                    html.P(
                        "Esta técnica captura relaciones semánticas complejas "
                        "y permite una mejor interpretación de las consultas."
                    ),
                    dbc.Alert(
                        "Resultado: Este método mejoró significativamente la similitud, "
                        "mostrando resultados de 89% a 69% en el top 10.",
                        color="success",
                        className="mt-3"
                    )
                ])
            ], className="h-100 shadow-sm")
        ])
    ], className="mb-4")

], fluid=True)