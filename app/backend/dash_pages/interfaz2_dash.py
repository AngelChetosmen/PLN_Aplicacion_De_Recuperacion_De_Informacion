# app/backend/dash_pages/interfaz2_dash.py

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from app.backend.Codigos.Procesamiento import preprocess_text
import torch
import base64
import io

dash.register_page(__name__, path='/analisis-bert', name='Análisis BERT')

# --- Lógica de Interfaz5.py copiada aquí ---
# Carga el modelo globalmente para evitar recargarlo en cada callback
# Esto puede tardar unos segundos la primera vez que se inicia la app
try:
    global_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # Modelo multilingüe ligero para español BERT
except Exception as e:
    print(f"Error al cargar SentenceTransformer: {e}")
    global_model = None

class PoemAnalyzer:
    def __init__(self, model):
        if model is None:
            raise ValueError("Modelo de SentenceTransformer no se pudo cargar.")
        self.model = model

    def load_corpus(self, path_or_buffer):
        """Carga el corpus desde un archivo CSV (ruta o buffer)."""
        self.df = pd.read_csv(path_or_buffer)
        if "normalized_content" not in self.df.columns:
            raise ValueError("El corpus no contiene la columna 'normalized_content'.")
        
        self.df['normalized_content'] = self.df['normalized_content'].fillna('')
        self.corpus_embeddings = self.model.encode(self.df['normalized_content'].tolist(), convert_to_tensor=True)

    def find_similar_poems(self, query, top_k=10):
        """Encuentra los poemas más similares a una consulta."""
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)
        
        top_results = torch.topk(cosine_scores.squeeze(0), k=min(top_k, len(self.df)))
        
        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            idx_item = idx.item()
            result = {
                'author': self.df.iloc[idx_item].get('author', 'N/A'),
                'title': self.df.iloc[idx_item].get('normalized_title', 'N/A'),
                'content': self.df.iloc[idx_item]['normalized_content'],
                'similarity': score.item(),
            }
            result['genre_prediction'] = self.predict_genre(result['content'])
            results.append(result)
        return results

    def predict_genre(self, content):
        """Predice el género basado en palabras clave simples."""
        # (Se omiten las listas de keywords por brevedad, pero deben estar aquí)
        romantic_keywords = {'princesa', 'castillo', 'amor', 'corazón', 'pasión'}
        horror_keywords = {'sangre', 'miedo', 'oscuridad', 'gritos', 'fantasma'}
        epopeya_keywords = {'héroe', 'gesta', 'batalla', 'viaje', 'dioses'}
        # ... y todas las demás listas de keywords de tu archivo original ...
        
        words = set(content.lower().split())
        
        if words.intersection(romantic_keywords):
            return "Romántico"
        elif words.intersection(horror_keywords):
            return "Horror"
        elif words.intersection(epopeya_keywords):
            return "Epopeya"
        # ... y todos los demás elif ...
        else:
            return "Desconocido"

# --- Fin de la lógica copiada ---


layout = dbc.Container([
    html.H2("Analizador de Poemas (SentenceTransformer BERT)"),
    
    dbc.Label("Cargar Corpus Normalizado (CSV):"),
    dcc.Upload(
        id='upload-corpus-bert',
        children=html.Div(['Arrastra y suelta o ', html.A('Selecciona un archivo')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        }
    ),
    dbc.Alert(id='corpus-load-status-bert', is_open=False, color="success"),
    
    dbc.Label("Poema de Prueba:", className="mt-3"),
    dbc.Textarea(id='query-text-bert', style={'height': 200}, placeholder="Escribe aquí el poema que deseas analizar..."),
    
    dbc.Row([
        dbc.Col(dbc.Button("Calcular Similitud", id='search-button-bert', color="primary"), width="auto"),
        dbc.Col(dbc.Button("Limpiar Poema", id='clear-poem-bert-button', color="secondary"), width="auto"),
        dbc.Col(dbc.Button("Limpiar Resultados", id='clear-results-bert-button', color="secondary"), width="auto"),
    ], className="mt-3 g-2"),
    
    dbc.Label("Resultados:", className="mt-3"),
    dcc.Loading(  
    type="default",
    children=dbc.Textarea(id='results-text-bert', readOnly=True, style={'height': 300})
),
    dbc.Alert(id='bert-error-alert', color="danger", is_open=False, className="mt-3")
])

# Callback para limpiar poema
@callback(
    Output('query-text-bert', 'value'),
    Input('clear-poem-bert-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_poem(n_clicks):
    return ""

# Callback para limpiar resultados
@callback(
    Output('results-text-bert', 'value'),
    Output('store-bert-results', 'data'),
    Input('clear-results-bert-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_results(n_clicks):
    return "", None

# Callback para mostrar estado de carga del corpus
@callback(
    Output('corpus-load-status-bert', 'children'),
    Output('corpus-load-status-bert', 'is_open'),
    Input('upload-corpus-bert', 'filename')
)
def update_corpus_status(filename):
    if filename:
        return f"Archivo '{filename}' listo para usar.", True
    return no_update, False

# Callback principal para calcular similitud
@callback(
    Output('results-text-bert', 'value', allow_duplicate=True),
    Output('store-bert-results', 'data', allow_duplicate=True),
    Output('bert-error-alert', 'children'),
    Output('bert-error-alert', 'is_open'),
    Input('search-button-bert', 'n_clicks'),
    State('query-text-bert', 'value'),
    State('upload-corpus-bert', 'contents'),
    prevent_initial_call=True
)
def search_bert_similarity(n_clicks, query, contents):
    if global_model is None:
        return no_update, no_update, "Error: El modelo SentenceTransformer no pudo cargarse.", True
    if not contents:
        return no_update, no_update, "Error: Carga un archivo de corpus.", True
    if not query:
        return no_update, no_update, "Error: Escribe un poema para analizar.", True

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_buffer = io.StringIO(decoded.decode('utf-8'))

    try:
        analyzer = PoemAnalyzer(global_model)
        analyzer.load_corpus(file_buffer)
        processed_query = preprocess_text(query)
        results = analyzer.find_similar_poems(processed_query, top_k=10)
        
        results_text_output = ""
        results_for_store = []
        
        for idx, res in enumerate(results):
            results_text_output += f"{idx + 1}.- Autor: {res['author']}\n"
            results_text_output += f"Título: {res['title']}\n"
            results_text_output += f"Similitud: {res['similarity']:.4f}\n"
            results_text_output += f"Género: {res['genre_prediction']}\n\n"
            
            results_for_store.append((res['title'], res['similarity']))
            
        return results_text_output, results_for_store, "", False

    except Exception as e:
        return no_update, no_update, f"Error durante el análisis: {e}", True