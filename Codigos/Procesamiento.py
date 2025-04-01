import pandas as pd
import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import tkinter as tk
from tkinter import filedialog, messagebox

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
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if file_path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, file_path)

# Función para ejecutar procesamiento
def process_corpus():
    input_path = entry_input.get()
    
    if not input_path:
        messagebox.showwarning("Advertencia", "Debe seleccionar un archivo de entrada.")
        return
    
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
    if not output_path:
        return  # Si el usuario cancela, no se hace nada
    
    normalize_and_save_corpus(input_path, output_path)

# Creación de la interfaz
top = tk.Tk()
top.title("Procesamiento de Corpus")
top.geometry("500x250")

# Etiqueta y campo para archivo de entrada
tk.Label(top, text="Archivo de entrada:").pack(pady=5)
entry_input = tk.Entry(top, width=50)
entry_input.pack()
tk.Button(top, text="Seleccionar archivo", command=load_file).pack(pady=5)

# Botón para procesar
tk.Button(top, text="Procesar Corpus", command=process_corpus, bg="green", fg="black").pack(pady=10)

# Ejecutar interfaz
top.mainloop()
