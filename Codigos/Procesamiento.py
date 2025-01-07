import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Configuración inicial
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))  # Stopwords en español

# Preprocesamiento del texto
def preprocess_text(text):
    """Aplica limpieza, tokenización, eliminación de stopwords y lematización al texto."""
    if pd.isna(text):
        return ""

    # Limpiar el texto
    text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', text)
    text = text.lower()

    # Tokenización
    tokens = nltk.word_tokenize(text)

    # Eliminar stopwords y lematizar
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    return ' '.join(tokens)

# Normalizar y guardar el corpus
def normalize_and_save_corpus(file_path, output_path):
    """Carga el corpus, normaliza el contenido y título, y guarda el nuevo corpus."""
    # Cargar datos
    df = pd.read_csv(file_path)

    # Normalizar las columnas "content" y "title"
    df['normalized_content'] = df['content'].apply(preprocess_text)
    df['normalized_title'] = df['title'].apply(preprocess_text)

    # Filtrar solo las columnas requeridas
    df = df[['author', 'normalized_content', 'normalized_title']]

    # Guardar el nuevo corpus
    df.to_csv(output_path, index=False)
    print(f"Corpus normalizado guardado en: {output_path}")

if __name__ == "__main__":
    # Ruta al archivo CSV del corpus
    input_file_path = "D:/Proyecto Final_PLN_Equipo11/Corpus/poems.csv"
    output_file_path = "D:/Proyecto Final_PLN_Equipo11/Corpus/poems_normalized.csv"

    # Normalizar y guardar el corpus
    normalize_and_save_corpus(input_file_path, output_file_path)
