# app/backend/Codigos/Representacion.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

def tfidf_vectorization(file_path_or_buffer, ngram_range=(1, 1)):
    """
    Carga un CSV normalizado y aplica vectorización TF-IDF.
    Acepta una ruta de archivo o un buffer de archivo (para archivos subidos).
    """
    try:
        df = pd.read_csv(file_path_or_buffer)
    except Exception as e:
        raise ValueError(f"Error al leer el archivo CSV: {e}")

    if 'normalized_content' not in df.columns:
        raise ValueError("El CSV debe tener la columna 'normalized_content'")

    # Asegurarse de que no haya NaNs, reemplazarlos con string vacío
    df['normalized_content'] = df['normalized_content'].fillna('')
    
    vectorizer = TfidfVectorizer(ngram_range=ngram_range)
    tfidf_matrix = vectorizer.fit_transform(df['normalized_content'])
    
    return df, vectorizer, tfidf_matrix

def calculate_cosine_similarity(tfidf_matrix):
    """Calcula la similitud del coseno de la matriz consigo misma."""
    return sklearn_cosine_similarity(tfidf_matrix)