import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import tkinter as tk
from tkinter import filedialog, messagebox

nltk.download('stopwords')
nltk.download('punkt')

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
def normalize_and_save_corpus(input_path, output_path):
    """Carga el corpus, normaliza el contenido y título, y guarda el nuevo corpus."""
    try:
        df = pd.read_csv(input_path)
        
        if 'content' not in df.columns or 'title' not in df.columns:
            messagebox.showerror("Error", "El archivo CSV debe contener las columnas 'content' y 'title'")
            return
        
        df['normalized_content'] = df['content'].apply(preprocess_text)
        df['normalized_title'] = df['title'].apply(preprocess_text)
        df = df[['author', 'normalized_content', 'normalized_title']]
        df.to_csv(output_path, index=False)
        
        messagebox.showinfo("Éxito", f"Corpus normalizado guardado en:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo: {str(e)}")

# Función para cargar archivo
def load_file(entry):
    """Muestra un cuadro de diálogo para seleccionar un archivo y actualiza la entrada."""
    file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Función para procesar el corpus
def process_corpus(entry):
    """Solicita la ubicación del archivo de salida y normaliza el corpus."""
    input_path = entry.get()
    if not input_path:
        messagebox.showwarning("Advertencia", "Debe seleccionar un archivo de entrada.")
        return
    
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
    if not output_path:
        return  # Si el usuario cancela, no se hace nada
    
    normalize_and_save_corpus(input_path, output_path)

# Función para crear la pestaña en la GUI principal
def create_procesamiento_ui(frame_procesamiento):
    """Crea la interfaz de la pestaña de procesamiento en la GUI principal."""
    tk.Label(frame_procesamiento, text="Archivo de entrada:").pack(pady=5)
    entry_input = tk.Entry(frame_procesamiento, width=50)
    entry_input.pack()

    tk.Button(frame_procesamiento, text="Seleccionar archivo", command=lambda: load_file(entry_input)).pack(pady=5)
    tk.Button(frame_procesamiento, text="Procesar Corpus", command=lambda: process_corpus(entry_input), bg="green", fg="black").pack(pady=10)
