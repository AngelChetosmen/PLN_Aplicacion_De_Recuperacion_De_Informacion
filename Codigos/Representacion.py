import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Representación de texto con TF-IDF
def tfidf_vectorization(file_path):
    """Carga el corpus normalizado y aplica TF-IDF vectorization."""
    # Cargar datos
    df = pd.read_csv(file_path)

    # Rellenar valores NaN con cadenas vacías
    df['normalized_content'] = df['normalized_content'].fillna("")
    df['normalized_title'] = df['normalized_title'].fillna("")

    # Concatenar contenido normalizado y título para representación conjunta
    combined_text = df['normalized_content'] + " " + df['normalized_title']

    # Vectorización TF-IDF con unigrama y bigrama
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(combined_text)

    return df, vectorizer, tfidf_matrix

# Calcular similitud de coseno
def calculate_cosine_similarity(tfidf_matrix):
    """Calcula la matriz de similitud de coseno para los textos vectorizados."""
    return cosine_similarity(tfidf_matrix)

if __name__ == "__main__":
    # Ruta al archivo CSV del corpus normalizado
    normalized_file_path = "D:/Proyecto Final_PLN_Equipo11/Corpus/poems_normalized.csv"  # Reemplaza con la ruta correcta

    # Ejecutar vectorización TF-IDF
    df, vectorizer, tfidf_matrix = tfidf_vectorization(normalized_file_path)

    # Mostrar un ejemplo de los términos y las dimensiones de la matriz
    print("Número de términos en la representación TF-IDF:", len(vectorizer.get_feature_names_out()))
    print("Dimensiones de la matriz TF-IDF:", tfidf_matrix.shape)

    # Calcular la similitud de coseno
    cosine_sim = calculate_cosine_similarity(tfidf_matrix)

    # Ejemplo de salida: Matriz de similitud de coseno para los primeros 5 textos
    print("\nMatriz de similitud de coseno (primeros 5x5):")
    print(cosine_sim[:5, :5])
