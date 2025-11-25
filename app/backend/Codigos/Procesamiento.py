# app/backend/Codigos/Procesamiento.py

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Descargar recursos de NLTK (puedes comentarlos después de la primera ejecución)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


# Configuración inicial
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))  # Stopwords en español

# Función para preprocesar texto
def preprocess_text(text):
    """Aplica limpieza, tokenización, eliminación de stopwords y lematización al texto."""
    if pd.isna(text):
        return ""

    text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', text)
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    return ' '.join(tokens)

# Función para normalizar y guardar el corpus
def normalize_and_save_corpus(input_path_or_buffer, output_path):
    """Carga el corpus, normaliza el contenido y título, y guarda el nuevo corpus."""
    try:
        # Lee desde un buffer (archivo subido) o una ruta de archivo
        df = pd.read_csv(input_path_or_buffer)
        
        if 'content' not in df.columns or 'title' not in df.columns:
            return "Error: El archivo CSV debe contener las columnas 'content' y 'title'"
        
        df['normalized_content'] = df['content'].apply(preprocess_text)
        df['normalized_title'] = df['title'].apply(preprocess_text)
        
        # Mantén 'author' si existe
        cols_to_save = ['normalized_content', 'normalized_title']
        if 'author' in df.columns:
            cols_to_save.insert(0, 'author')
            
        df_normalized = df[cols_to_save]
        
        # Guarda en la ruta de salida
        df_normalized.to_csv(output_path, index=False)
        
        return f"Éxito: Corpus normalizado guardado en: {output_path}"
    except Exception as e:
        return f"Error: No se pudo procesar el archivo: {str(e)}"