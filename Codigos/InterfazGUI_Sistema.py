import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Interfaz2  # Importar la interfaz 2
import Interfaz5  # Importar la interfaz 5
import Procesamiento  # Importar el módulo de procesamiento

class PLNApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Recuperación de Información de Poemas")

        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Crear pestañas
        self.create_procesamiento_tab()
        self.create_interfaz2_tab()
        self.create_interfaz5_tab()
        self.create_resultados_tab()

    def create_procesamiento_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Procesamiento")
        frame_procesamiento = ttk.Frame(tab)
        frame_procesamiento.pack(expand=True, fill="both", padx=10, pady=10)
        Procesamiento.create_procesamiento_ui(frame_procesamiento)

    def create_interfaz2_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Analizador de Poemas Similitud Coseno")
        frame_interfaz2 = ttk.Frame(tab)
        frame_interfaz2.pack(expand=True, fill="both", padx=10, pady=10)
        self.interfaz2 = Interfaz2.PoemAnalyzerApp(frame_interfaz2)

    def create_interfaz5_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Analizador de Poemas BERT")
        frame_interfaz5 = ttk.Frame(tab)
        frame_interfaz5.pack(expand=True, fill="both", padx=10, pady=10)
        self.interfaz5 = Interfaz5.PoemAnalyzerApp(frame_interfaz5)

    def create_resultados_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Resultados")

        # Campos de texto para mostrar resultados
        ttk.Label(tab, text="Resultados Similitud Coseno").pack()
        self.result_text_coseno = tk.Text(tab, height=10, width=50)
        self.result_text_coseno.pack()
        ttk.Label(tab, text="Resultados BERT").pack()
        self.result_text_bert = tk.Text(tab, height=10, width=50)
        self.result_text_bert.pack()

        # Botones para limpiar resultados
        ttk.Button(tab, text="Limpiar Resultados", command=self.clear_results).pack(pady=5)
        ttk.Button(tab, text="Actualizar Gráfica", command=self.update_graph).pack(pady=5)

        # Espacio para la gráfica
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=tab)
        self.canvas.get_tk_widget().pack()

    def clear_results(self):
        self.result_text_coseno.delete(1.0, tk.END)
        self.result_text_bert.delete(1.0, tk.END)

    def update_graph(self):
        self.ax.clear()
        
        # Obtener datos de las interfaces
        data_coseno = self.interfaz2.get_top_10()  # Debe devolver una lista de (posición, similitud)
        data_bert = self.interfaz5.get_top_10()  # Debe devolver una lista de (posición, similitud)

        if data_coseno:
            x_coseno, y_coseno = zip(*data_coseno)
            self.ax.plot(x_coseno, y_coseno, marker='o', linestyle='-', label='Similitud Coseno', color='blue')
        
        if data_bert:
            x_bert, y_bert = zip(*data_bert)
            self.ax.plot(x_bert, y_bert, marker='s', linestyle='-', label='Similitud BERT', color='red')
        
        self.ax.set_xlabel("Poema")
        self.ax.set_ylabel("Similitud")
        self.ax.set_title("Comparación de Similitud de Poemas")
        self.ax.set_xticks(range(1, 11))
        self.ax.set_ylim(0, 1)
        self.ax.legend()
        self.canvas.draw()

if __name__ == "_main_":
    root = tk.Tk()
    app = PLNApp(root)
    root.mainloop()