import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
from Procesamiento import normalize_and_save_corpus  # Asegúrate de que Procesamiento.py esté en el mismo directorio
from Representacion import tfidf_vectorization, calculate_cosine_similarity

import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.corpus import stopwords



class PoemAnalyzerApp:
    def __init__(self, master):
        self.master = master
        if isinstance(master,tk.Tk):
            master.title("Analizador de Poemas")

        # Cargar corpus normalizado
        self.label_normalized_corpus = tk.Label(master, text="Cargar Corpus Normalizado:")
        self.label_normalized_corpus.pack()
        self.normalized_corpus_path = tk.Entry(master, width=50)
        self.normalized_corpus_path.pack()
        self.button_load_normalized = tk.Button(master, text="Cargar", command=self.load_normalized_corpus)
        self.button_load_normalized.pack()

        # Selección de n-gramas
        self.label_ngram = tk.Label(master, text="Seleccionar N-gramas:")
        self.label_ngram.pack()
        self.ngram_var = tk.StringVar(value='unigram')
        self.radio_unigram = tk.Radiobutton(master, text='Unigramas', variable=self.ngram_var, value='unigram')
        self.radio_bigram = tk.Radiobutton(master, text='Bigramas', variable=self.ngram_var, value='bigram')
        self.radio_unigram.pack()
        self.radio_bigram.pack()

        # Campo para ingresar poema
        self.label_poem = tk.Label(master, text="Escribir Poema:")
        self.label_poem.pack()
        self.poem_text = scrolledtext.ScrolledText(master, width=60, height=10)
        self.poem_text.pack()

        # Botones
        self.button_help = tk.Button(master, text="Ayuda", command=self.show_help)
        self.button_help.pack()

        # Cambiar texto del botón a "Calcular similitud"
        self.button_calculate_similarity = tk.Button(master, text="Calcular similitud", command=self.analyze_poem)
        self.button_calculate_similarity.pack()

        # Botón para limpiar el campo de poema
        self.button_clear_poem = tk.Button(master, text="Limpiar Poema", command=self.clear_poem)
        self.button_clear_poem.pack()

        # Botón para limpiar resultados
        self.button_clear_results = tk.Button(master, text="Limpiar Resultados", command=self.clear_results)
        self.button_clear_results.pack()

        # Área para mostrar resultados
        self.results_area = scrolledtext.ScrolledText(master, width=80, height=10)
        self.results_area.pack()

    def load_raw_corpus(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.raw_corpus_path.delete(0, tk.END)
            self.raw_corpus_path.insert(0, file_path)

    def load_normalized_corpus(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.normalized_corpus_path.delete(0, tk.END)
            self.normalized_corpus_path.insert(0, file_path)

    def show_help(self):
        messagebox.showinfo("Ayuda", "Esta aplicación permite analizar poemas y encontrar similitudes con otros poemas en el corpus.")

    def clear_poem(self):
        """Limpia el campo de texto del poema."""
        self.poem_text.delete("1.0", tk.END)

    def clear_results(self):
        """Limpia el área de resultados."""
        self.results_area.delete("1.0", tk.END)

    def analyze_poem(self):
        #raw_file_path = self.raw_corpus_path.get()
        normalized_file_path = self.normalized_corpus_path.get()
        
        # Normalizar el corpus si no se ha proporcionado uno normalizado
        if not normalized_file_path:
            output_file_path = "normalized_poems.csv"
            normalize_and_save_corpus(output_file_path)
            normalized_file_path = output_file_path
        
        # Vectorización TF-IDF
        df, vectorizer, tfidf_matrix = tfidf_vectorization(normalized_file_path)

        # Ingresar poema y vectorizarlo
        input_poem = self.poem_text.get("1.0", tk.END).strip()
        
        if input_poem:
            input_vector = vectorizer.transform([input_poem])  # Vectorizar el poema ingresado
            
            # Calcular similitud coseno entre el poema ingresado y todos los poemas del corpus
            cosine_similarities = calculate_cosine_similarity(tfidf_matrix)  # Matriz de similitudes del corpus
            
            # Añadir el vector del poema ingresado a la matriz de similitudes
            combined_matrix = tfidf_matrix.copy()  # Copiar la matriz existente
            
            # Concatenar usando scipy sparse matrix para evitar problemas de memoria
            from scipy.sparse import vstack
            combined_matrix = vstack([combined_matrix, input_vector])  # Combinar matrices

            cosine_similarities_combined = calculate_cosine_similarity(combined_matrix)  # Calcular nuevas similitudes

            poem_similarities_combined = cosine_similarities_combined[-1]  # Última fila corresponde al poema ingresado
            
            # Obtener los índices de los 10 poemas más similares (excluyendo el último que es el poema ingresado)
            similar_indices = poem_similarities_combined[:-1].argsort()[-10:][::-1]  # Top 10
            
            results_text = "Top 10 Poemas Similares:\n"
            for idx, index in enumerate(similar_indices):
                line_number = index + 1  # +1 para mostrar la línea en formato humano (1-indexado)
                results_text += f"{idx + 1}. {df['normalized_title'][index]} - Línea: {line_number} - Similitud: {poem_similarities_combined[index]:.4f}\n"
            
            # Mostrar resultados
            self.results_area.delete("1.0", tk.END)  # Limpiar área de resultados antes de mostrar nuevos resultados
            self.results_area.insert(tk.END, results_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PoemAnalyzerApp(root)
    root.mainloop()
