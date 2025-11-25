# app/backend/dash_pages/procesamiento.py

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import base64
import io

# Importa la lógica refactorizada
from Codigos.Procesamiento import normalize_and_save_corpus

dash.register_page(__name__, path='/procesamiento', name='Procesamiento')

layout = dbc.Container([
    html.H2("Procesamiento de Corpus"),
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-raw-corpus',
                children=html.Div(['Arrastra y suelta o ', html.A('Selecciona un archivo CSV')]),
                style={
                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                },
                multiple=False
            ),
        ], width=6),
        dbc.Col([
            dbc.Input(
                id='output-filename', 
                placeholder="Nombre del archivo de salida (e.g., normalized_corpus.csv)", 
                value="normalized_corpus.csv"
            ),
        ], width=6)
    ]),
    dbc.Button("Procesar Corpus", id='process-button', color="primary", className="mt-2"),
    dbc.Alert(id='process-output-message', color="info", is_open=False, className="mt-3")
])

@callback(
    Output('process-output-message', 'children'),
    Output('process-output-message', 'is_open'),
    Output('process-output-message', 'color'),
    Input('process-button', 'n_clicks'),
    State('upload-raw-corpus', 'contents'),
    State('upload-raw-corpus', 'filename'),
    State('output-filename', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, contents, filename, output_name):
    if not contents:
        return "Error: No se ha seleccionado ningún archivo.", True, "danger"
    if not output_name:
        return "Error: Debes especificar un nombre de archivo de salida.", True, "danger"

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        # Usa io.StringIO para que pandas lea el contenido decodificado como un archivo
        file_buffer = io.StringIO(decoded.decode('utf-8'))
        
        # Llama a la lógica de procesamiento
        # Nota: Esta función ahora guarda en el servidor.
        # Para una app web real, querrías ofrecer esto como una descarga.
        # Por ahora, lo guardará en la carpeta donde se ejecuta el servidor.
        message = normalize_and_save_corpus(file_buffer, output_name)
        
        if message.startswith("Éxito"):
            return message, True, "success"
        else:
            return message, True, "warning"
            
    except Exception as e:
        return f"Error crítico al procesar: {e}", True, "danger"