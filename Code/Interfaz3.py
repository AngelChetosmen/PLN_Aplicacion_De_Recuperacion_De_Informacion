import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
import tkinter as tk
from tkinter import filedialog, messagebox

class PoemAnalyzer:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def load_corpus(self, path):
        """
        Carga el corpus desde un archivo CSV.
        """
        self.df = pd.read_csv(path)

        if "normalized_content" not in self.df.columns:
            raise ValueError("El corpus no contiene la columna necesaria: 'normalized_content'.")

        self.corpus_embeddings = self.model.encode(self.df['normalized_content'].tolist(), convert_to_tensor=True)

    def find_similar_poems(self, query, top_k=5):
        """
        Encuentra los poemas más similares a una consulta.
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)

        # Obtener los valores y los índices de los top_k resultados
        top_results = torch.topk(cosine_scores.squeeze(0), k=top_k)

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            result = {
                'author': self.df.iloc[idx.item()]['author'],
                'title': self.df.iloc[idx.item()]['normalized_title'],
                'content': self.df.iloc[idx.item()]['normalized_content'],
                'similarity': score.item()
            }
            results.append(result)
        return results

class PoemAnalyzerApp:
    def __init__(self, root):
        self.analyzer = PoemAnalyzer()
        self.root = root
        self.root.title("Poem Analyzer")

        # Botón para cargar el corpus
        self.load_button = tk.Button(root, text="Cargar Corpus", command=self.load_corpus)
        self.load_button.pack(pady=10)

        # Entrada para la consulta
        self.query_label = tk.Label(root, text="Escribe tu consulta:")
        self.query_label.pack()
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack(pady=5)

        # Botón para buscar poemas similares
        self.search_button = tk.Button(root, text="Buscar Poemas Similares", command=self.search_poems)
        self.search_button.pack(pady=10)

        # Área de texto para mostrar los resultados
        self.results_text = tk.Text(root, height=20, width=80)
        self.results_text.pack(pady=10)

    def load_corpus(self):
        """
        Abre un diálogo para seleccionar y cargar el archivo del corpus.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            self.analyzer.load_corpus(file_path)
            messagebox.showinfo("Éxito", "Corpus cargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el corpus: {e}")

    def search_poems(self):
        """
        Busca poemas similares basados en la consulta ingresada.
        """
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una consulta.")
            return

        try:
            results = self.analyzer.find_similar_poems(query, top_k=5)
            self.results_text.delete(1.0, tk.END)

            if results:
                for result in results:
                    self.results_text.insert(tk.END, f"Autor: {result['author']}\n")
                    self.results_text.insert(tk.END, f"Título: {result['title']}\n")
                    self.results_text.insert(tk.END, f"Contenido: {result['content']}\n")
                    self.results_text.insert(tk.END, f"Similitud: {result['similarity']:.4f}\n\n")
            else:
                self.results_text.insert(tk.END, "No se encontraron resultados similares.\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PoemAnalyzerApp(root)
    root.mainloop()
