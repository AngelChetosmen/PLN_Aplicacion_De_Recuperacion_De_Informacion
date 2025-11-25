# app/backend/dash_pages/interfaz1_dash.py

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from scipy.sparse import vstack
import base64
import io

# Importa la lógica refactorizada
from app.backend.Codigos.Representacion import tfidf_vectorization, calculate_cosine_similarity
from app.backend.Codigos.Procesamiento import preprocess_text # Para procesar el poema de entrada

dash.register_page(__name__, path='/similitud-coseno', name='Similitud Coseno')

layout = dbc.Container([
    html.H2("Analizador de Poemas (TF-IDF + Similitud Coseno)"),
    
    dbc.Label("Cargar Corpus Normalizado (CSV):"),
    dcc.Upload(
        id='upload-normalized-corpus-tfidf',
        children=html.Div(['Arrastra y suelta o ', html.A('Selecciona un archivo')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        }
    ),
    
    dbc.Label("Seleccionar N-gramas:"),
    dbc.RadioItems(
        options=[
            {'label': 'Unigramas', 'value': 'unigram'},
            {'label': 'Bigramas', 'value': 'bigram'},
        ],
        value='unigram',
        id='ngram-var-tfidf',
        inline=True
    ),
    
    dbc.Label("Escribir Poema:", className="mt-3"),
    dbc.Textarea(id='poem-input-tfidf', style={'height': 200}, placeholder="Escribe aquí el poema que deseas analizar..."),
    
    dbc.Row([
        dbc.Col(dbc.Button("Calcular Similitud", id='calc-sim-tfidf-button', color="primary"), width="auto"),
        dbc.Col(dbc.Button("Limpiar Poema", id='clear-poem-tfidf-button', color="secondary"), width="auto"),
        dbc.Col(dbc.Button("Limpiar Resultados", id='clear-results-tfidf-button', color="secondary"), width="auto"),
        dbc.Col(dbc.Button("Ayuda", id='help-button-tfidf', color="info"), width="auto"),
    ], className="mt-3 g-2"),
    
    dbc.Collapse(
        dbc.Alert("Esta aplicación permite analizar poemas y encontrar similitudes con otros poemas en el corpus usando TF-IDF.", color="info"),
        id="help-collapse-tfidf",
        is_open=False,
        className="mt-3"
    ),
    
    dbc.Label("Resultados:", className="mt-3"),
    dcc.Loading(
        type="default",
        children=dbc.Textarea(id='results-area-tfidf', readOnly=True, style={'height': 300}, placeholder="Los resultados aparecerán aqui...")
    ),
    dbc.Alert(id='tfidf-error-alert', color="danger", is_open=False, className="mt-3")
])

# Callback para el botón de Ayuda
@callback(
    Output("help-collapse-tfidf", "is_open"),
    Input("help-button-tfidf", "n_clicks"),
    State("help-collapse-tfidf", "is_open"),
    prevent_initial_call=True
)
def toggle_help(n, is_open):
    return not is_open if n else is_open

# Callback para limpiar poema
@callback(
    Output('poem-input-tfidf', 'value'),
    Input('clear-poem-tfidf-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_poem(n_clicks):
    return ""

# Callback para limpiar resultados
@callback(
    Output('results-area-tfidf', 'value'),
    Output('store-cosine-results', 'data'),
    Input('clear-results-tfidf-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_results(n_clicks):
    return "", None

# Callback principal para calcular similitud
@callback(
    Output('results-area-tfidf', 'value', allow_duplicate=True),
    Output('store-cosine-results', 'data', allow_duplicate=True),
    Output('tfidf-error-alert', 'children'),
    Output('tfidf-error-alert', 'is_open'),
    Input('calc-sim-tfidf-button', 'n_clicks'),
    State('upload-normalized-corpus-tfidf', 'contents'),
    State('ngram-var-tfidf', 'value'),
    State('poem-input-tfidf', 'value'),
    prevent_initial_call=True
)
def calculate_tfidf_similarity(n_clicks, contents, ngram_value, poem_text):
    if not contents:
        return no_update, no_update, "Error: Carga un archivo de corpus normalizado.", True
    if not poem_text:
        return no_update, no_update, "Error: Escribe un poema para analizar.", True

    ngram_range = (1, 1) if ngram_value == 'unigram' else (1, 2)
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_buffer = io.StringIO(decoded.decode('utf-8'))

    try:
        # 1. Vectorización TF-IDF
        df, vectorizer, tfidf_matrix = tfidf_vectorization(file_buffer, ngram_range)

        # 2. Procesar y vectorizar el poema de entrada
        processed_poem = preprocess_text(poem_text)
        input_vector = vectorizer.transform([processed_poem])
        
        # 3. Combinar matrices
        combined_matrix = vstack([tfidf_matrix, input_vector])

        # 4. Calcular similitud coseno
        cosine_similarities_combined = calculate_cosine_similarity(combined_matrix)
        
        # 5. Obtener similitudes del poema ingresado (última fila)
        poem_similarities = cosine_similarities_combined[-1]
        
        # 6. Obtener top 10 (excluyendo el último que es el poema mismo)
        similar_indices = poem_similarities[:-1].argsort()[-10:][::-1]
        
        results_text = "Top 10 Poemas Similares:\n"
        results_for_store = []
        
        for idx, index in enumerate(similar_indices):
            title = df['normalized_title'].iloc[index] if 'normalized_title' in df.columns else f"Poema {index}"
            similarity = poem_similarities[index]
            
            results_text += f"{idx + 1}. {title} - Similitud: {similarity:.4f}\n"
            results_for_store.append((title, similarity))
        
        return results_text, results_for_store, "", False

    except Exception as e:
        return no_update, no_update, f"Error durante el análisis: {e}", True