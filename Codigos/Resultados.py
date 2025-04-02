import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Interfaz2 import PoemAnalyzerApp as get_cosine_top_10
from Interfaz5 import PoemAnalyzer as get_bert_top_10

def mostrar_resultados():
    # Obtener datos de ambos modelos
    top_10_cosine = get_cosine_top_10()
    top_10_bert = get_bert_top_10()
    
    # Mostrar resultados en los campos de texto
    campo_cosine.delete("1.0", tk.END)
    campo_bert.delete("1.0", tk.END)
    for idx, (poema, sim) in enumerate(top_10_cosine, start=1):
        campo_cosine.insert(tk.END, f"{idx}. {poema}: {sim}\n")
    for idx, (poema, sim) in enumerate(top_10_bert, start=1):
        campo_bert.insert(tk.END, f"{idx}. {poema}: {sim}\n")
    
    # Actualizar gráfica
    actualizar_grafica(top_10_cosine, top_10_bert)

def limpiar_campos():
    campo_cosine.delete("1.0", tk.END)
    campo_bert.delete("1.0", tk.END)
    ax.clear()
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Poema")
    ax.set_ylabel("Similitud")
    canvas.draw()

def actualizar_grafica(top_10_cosine, top_10_bert):
    ax.clear()
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Poema")
    ax.set_ylabel("Similitud")
    
    # Extraer coordenadas para la gráfica
    x_cosine = list(range(1, 11))
    y_cosine = [sim for _, sim in top_10_cosine]
    x_bert = list(range(1, 11))
    y_bert = [sim for _, sim in top_10_bert]
    
    ax.plot(x_cosine, y_cosine, marker='o', linestyle='-', label="Cosine", color='blue')
    ax.plot(x_bert, y_bert, marker='s', linestyle='-', label="BERT", color='red')
    ax.legend()
    
    canvas.draw()

# Crear ventana principal
root = tk.Tk()
root.title("Resultados")

# Crear pestaña de resultados
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Campos de texto para mostrar resultados
campo_cosine = tk.Text(frame, height=10, width=40)
campo_cosine.pack(side=tk.LEFT, padx=5)
campo_bert = tk.Text(frame, height=10, width=40)
campo_bert.pack(side=tk.RIGHT, padx=5)

# Botones
btn_mostrar = ttk.Button(frame, text="Mostrar Resultados", command=mostrar_resultados)
btn_mostrar.pack()
btn_limpiar = ttk.Button(frame, text="Limpiar", command=limpiar_campos)
btn_limpiar.pack()

# Área de gráfica
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Ejecutar aplicación
root.mainloop()
