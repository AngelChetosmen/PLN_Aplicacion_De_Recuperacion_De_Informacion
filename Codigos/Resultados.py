import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Interfaz2 import PoemAnalyzerApp as get_cosine_top_10
from Interfaz5 import PoemAnalyzer as get_bert_top_10

# Variables globales para la gráfica
fig, ax = plt.subplots()
canvas = None

def mostrar_resultados(frame):
    """Crea la interfaz de resultados en el marco proporcionado."""
    global canvas
    global ax

    # Crear campos de texto para mostrar resultados
    campo_cosine = tk.Text(frame, height=10, width=40)
    campo_cosine.pack(side=tk.LEFT, padx=5)
    campo_bert = tk.Text(frame, height=10, width=40)
    campo_bert.pack(side=tk.RIGHT, padx=5)

    # Botones
    btn_mostrar = ttk.Button(frame, text="Mostrar Resultados", command=lambda: mostrar_resultados_en_campos(campo_cosine, campo_bert))
    btn_mostrar.pack()
    btn_limpiar = ttk.Button(frame, text="Limpiar", command=lambda: limpiar_campos(campo_cosine, campo_bert))
    btn_limpiar.pack()

    # Crear área de gráfica y colocarla debajo de los campos de resultados
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(pady=10)  # Añadir un poco de espacio arriba de la gráfica

def mostrar_resultados_en_campos(campo_cosine, campo_bert):
    """Muestra los resultados en los campos de texto."""
    # Obtener datos de ambos modelos
    top_10_cosine = get_cosine_top_10()
    top_10_bert = get_bert_top_10()
    
    # Mostrar resultados en los campos de texto
    campo_cosine.delete("1.0", tk.END)
    campo_bert.delete("1.0", tk.END)
    
    # Procesar y mostrar resultados de similitud coseno
    cosine_similarities = []
    for idx, (poema, sim) in enumerate(top_10_cosine, start=1):
        campo_cosine.insert(tk.END, f"{idx}. {poema}: {sim:.4f}\n")
        cosine_similarities.append(sim)

    # Procesar y mostrar resultados de BERT
    bert_similarities = []
    for idx, (poema, sim) in enumerate(top_10_bert, start=1):
        campo_bert.insert(tk.END, f"{idx}. {poema}: {sim:.4f}\n")
        bert_similarities.append(sim)

    # Actualizar gráfica
    actualizar_grafica(cosine_similarities, bert_similarities)

def limpiar_campos(campo_cosine, campo_bert):
    """Limpia los campos de texto y la gráfica."""
    campo_cosine.delete("1.0", tk.END)
    campo_bert.delete("1.0", tk.END)
    ax.clear()
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Poema")
    ax.set_ylabel("Similitud")
    canvas.draw()

def actualizar_grafica(cosine_similarities, bert_similarities):
    """Actualiza la gráfica con los datos de similitud."""
    ax.clear()
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Poema")
    ax.set_ylabel("Similitud")
    
    # Extraer coordenadas para la gráfica
    x_cosine = list(range(1, len(cosine_similarities) + 1))
    y_cosine = cosine_similarities
    x_bert = list(range(1, len(bert_similarities) + 1))
    y_bert = bert_similarities
    
    ax.plot(x_cosine, y_cosine, marker='o', linestyle='-', label="Similitud Coseno", color='blue')
    ax.plot(x_bert, y_bert, marker='s', linestyle='-', label="Similitud BERT", color='red')
    ax.legend()
    
    canvas.draw()

# Nota: No se crea una ventana principal aquí, ya que se espera que se llame desde InterfazGUI_Sistema.py