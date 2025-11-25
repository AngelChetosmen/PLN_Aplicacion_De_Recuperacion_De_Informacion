# app/backend/dash_pages/resultados.py

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

dash.register_page(__name__, path='/resultados', name='Resultados')

layout = dbc.Container([
    html.H2("Resultados Comparativos"),
    
    dbc.Row([
        dbc.Col(dbc.Button("Mostrar Resultados", id='show-results-button', color="primary"), width="auto"),
        dbc.Col(dbc.Button("Limpiar Todo", id='clear-all-results-button', color="danger"), width="auto"),
    ], className="mt-3 g-2"),
    
    dbc.Row([
        dbc.Col([
            dbc.Label("Resultados Similitud Coseno (TF-IDF)"),
            dbc.Textarea(id='results-cosine-display', readOnly=True, style={'height': 300})
        ], width=6),
        dbc.Col([
            dbc.Label("Resultados Similitud (BERT)"),
            dbc.Textarea(id='results-bert-display', readOnly=True, style={'height': 300})
        ], width=6)
    ], className="mt-3"),
    
    dbc.Row([
        dbc.Col([
            # CAMBIO: Esto ahora es un Div vacío en lugar de un dcc.Graph
            # El gráfico se insertará aquí mediante el callback.
            html.Div(id='graph-output-container')
        ], width=12)
    ], className="mt-3")
])

# Callback para Limpiar
@callback(
    Output('results-cosine-display', 'value'),
    Output('results-bert-display', 'value'),
    Output('graph-output-container', 'children'), # <-- CAMBIO: Apunta al 'children' del Div
    Output('store-cosine-results', 'clear_data'), 
    Output('store-bert-results', 'clear_data'),   
    Input('clear-all-results-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_all(n_clicks):
    # Devolvemos un string vacío para limpiar el gráfico
    return "", "", "", True, True

# Callback para Mostrar Resultados
@callback(
    Output('results-cosine-display', 'value', allow_duplicate=True),
    Output('results-bert-display', 'value', allow_duplicate=True),
    Output('graph-output-container', 'children', allow_duplicate=True), # <-- CAMBIO: Apunta al 'children' del Div
    Input('show-results-button', 'n_clicks'),
    State('store-cosine-results', 'data'),
    State('store-bert-results', 'data'),
    prevent_initial_call=True
)
def show_results(n_clicks, cosine_data, bert_data):
    cosine_text = "No hay datos de Similitud Coseno."
    bert_text = "No hay datos de BERT."
    
    fig = go.Figure()
    
    if cosine_data:
        cosine_text = ""
        y_cosine = []
        for idx, (poema, sim) in enumerate(cosine_data, start=1):
            cosine_text += f"{idx}. {poema}: {sim:.4f}\n"
            y_cosine.append(sim)
        
        x_cosine = list(range(1, len(y_cosine) + 1))
        fig.add_trace(go.Scatter(x=x_cosine, y=y_cosine, mode='lines+markers', name='Similitud Coseno (TF-IDF)'))

    if bert_data:
        bert_text = ""
        y_bert = []
        for idx, (poema, sim) in enumerate(bert_data, start=1):
            bert_text += f"{idx}. {poema}: {sim:.4f}\n"
            y_bert.append(sim)
        
        x_bert = list(range(1, len(y_bert) + 1))
        fig.add_trace(go.Scatter(x=x_bert, y=y_bert, mode='lines+markers', name='Similitud (BERT)'))
    
    fig.update_layout(
        title="Comparativa de Similitud",
        xaxis_title="Top N Poemas",
        yaxis_title="Similitud",
        yaxis_range=[0, 1]
    )
    
    # CAMBIO: En lugar de solo la figura, devolvemos el componente dcc.Graph completo
    return cosine_text, bert_text, dcc.Graph(figure=fig)