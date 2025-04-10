# InterfazGUI_Sistema.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Interfaz2  # Importar la interfaz 2
import Interfaz5  # Importar la interfaz 5
import Procesamiento 
import Resultados

class PLNApp:
    def __init__(self, root):
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
        frame_resultados = ttk.Frame(tab)
        frame_resultados.pack(expand=True, fill="both", padx=10, pady=10)
        Resultados.mostrar_resultados(frame_resultados)  # Llamar a la función para mostrar resultados

if __name__ == "__main__":
    root = tk.Tk()
    app = PLNApp(root)
    root.mainloop()