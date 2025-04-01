import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Interfaz2  # Importar la interfaz 2 desde el repositorio
import Interfaz5  # Importar la interfaz 5 desde el repositorio

class PLNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recuperación de Información de Poemas")  # Título de la ventana principal

        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Crear pestañas
        self.create_procesamiento_tab()
        self.create_interfaz2_tab()
        self.create_interfaz5_tab()
        self.create_resultados_tab()

    def create_procesamiento_tab(self):
        """ Crea la pestaña de procesamiento. """
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Procesamiento")

        ttk.Label(tab, text="Cargar Corpus").pack(pady=10)
        ttk.Button(tab, text="Seleccionar CSV", command=self.load_corpus).pack()
        self.status_label = ttk.Label(tab, text="Estado: Esperando archivo...")
        self.status_label.pack(pady=10)

    def load_corpus(self):
        """ Carga y normaliza un archivo CSV. """
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                processed_file = "corpus_normalizado.csv"
                df.to_csv(processed_file, index=False)
                self.status_label.config(text="Estado: Corpus normalizado y guardado")
                messagebox.showinfo("Éxito", "Corpus normalizado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

    def create_interfaz2_tab(self):
        """ Crea la pestaña de Interfaz 2 e incrusta su contenido. """
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Analizador de Poemas Similitud Coseno")

        # Contenedor para Interfaz2
        frame_interfaz2 = ttk.Frame(tab)
        frame_interfaz2.pack(expand=True, fill="both", padx=10, pady=10)

        # Inicializar la interfaz dentro del contenedor
        Interfaz2.PoemAnalyzerApp(frame_interfaz2)  # Llama a la interfaz 2 tal como está

    def create_interfaz5_tab(self):

        # Contenedor para Interfaz5
        frame_interfaz5 = tk.Frame(self.notebook)
        frame_interfaz5.pack(expand=True, fill="both", padx=10, pady=10)

        # Inicializar la interfaz dentro del contenedor
        Interfaz5.PoemAnalyzerApp(frame_interfaz5)  # Llama a la interfaz 5 tal como está
        self.notebook.add(frame_interfaz5,text="Analizador de Poemas BERT")

    def create_resultados_tab(self):
        """ Crea la pestaña de resultados. """
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Resultados")

        ttk.Label(tab, text="Resultados de las Interfaz 2 y 5").pack(pady=10)
        self.result_text = tk.Text(tab, height=10, width=50)
        self.result_text.pack()
        ttk.Button(tab, text="Limpiar Resultados", command=self.clear_results).pack(pady=5)

        # Gráfica
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Similitud de Poemas")
        self.ax.set_xlabel("Poemas")
        self.ax.set_ylabel("Similitud (%)")
        self.canvas = FigureCanvasTkAgg(self.fig, tab)
        self.canvas.get_tk_widget().pack()

        ttk.Button(tab, text="Limpiar Gráfica", command=self.clear_plot).pack(pady=5)

    def clear_results(self):
        """ Limpia el área de resultados. """
        self.result_text.delete(1.0, tk.END)

    def clear_plot(self):
        """ Limpia la gráfica de resultados. """
        self.ax.clear()
        self.ax.set_title("Similitud de Poemas")
        self.ax.set_xlabel("Poemas")
        self.ax.set_ylabel("Similitud (%)")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PLNApp(root)
    root.mainloop()