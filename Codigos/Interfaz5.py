import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class PoemAnalyzer:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def load_corpus(self, path):
        """Carga el corpus desde un archivo CSV."""
        self.df = pd.read_csv(path)
        if "normalized_content" not in self.df.columns:
            raise ValueError("El corpus no contiene la columna necesaria: 'normalized_content'.")
        self.corpus_embeddings = self.model.encode(self.df['normalized_content'].tolist(), convert_to_tensor=True)

    def find_similar_poems(self, query, top_k=10):
        """Encuentra los poemas más similares a una consulta."""
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)
        
        top_results = torch.topk(cosine_scores.squeeze(0), k=top_k)
        
        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            result = {
                'author': self.df.iloc[idx.item()]['author'],
                'title': self.df.iloc[idx.item()]['normalized_title'],
                'content': self.df.iloc[idx.item()]['normalized_content'],
                'similarity': score.item(),
                'line_number': idx.item() + 1  # Línea en el corpus (1-indexado)
            }
            result['classification_words'] = self.get_classification_words(result['content'])
            results.append(result)
        return results

    def get_classification_words(self, content):
        """Obtiene palabras relevantes del contenido para la clasificación (verbos en infinitivo)."""
        words = content.split()
        classification_words = [word for word in words if word.lower() in {'besar', 'matar', 'rogar', 'extrañar', 'sonreír', 'amar', 'desear'}]
        return classification_words

    def extract_keywords(self, content):
        """Extrae palabras clave simples del contenido."""
        words = content.split()
        return list(set(words))[:5]  # Retorna las primeras 5 palabras únicas

    def predict_genre(self, content):
        """Predice el género basado en palabras clave simples."""
        epopeya_keywords = {
            'héroe', 'gesta', 'batalla', 'viaje', 'dioses', 'pueblo', 'aventura', 'proeza', 
            'reyes', 'valentía', 'gloria', 'epopeya', 'espada', 'enemigos', 'sacrificio', 
            'honor', 'leyenda', 'tradición', 'destino', 'hazañas', 'misión', 'epílogo', 
            'coraje', 'saga', 'triunfo', 'fuerza', 'desafío', 'guerrero', 'resistencia', 
            'origen', 'familia', 'guerras', 'victoria', 'río', 'montañas', 'destreza', 
            'campañas', 'historia', 'antigüedad', 'oráculo', 'conquista', 'imperio', 
            'salvación', 'juramento', 'espíritu', 'honra', 'poder', 'cantos', 'narración', 
            'hazaña', 'reinos', 'sabiduría', 'consejo', 'tormenta', 'superación', 'desafío',
            'simbología', 'rebelión', 'fidelidad', 'diálogo', 'artefactos', 'conflictos', 
            'sociedad', 'riqueza', 'fundación', 'legado', 'redención', 'mar', 'profecía', 
            'ritual', 'destierro', 'pruebas', 'exilio', 'lealtad', 'compasión', 'ética', 
            'valores', 'sabio', 'estrella', 'eternidad', 'sangre', 'rivalidad', 'épico', 
            'espíritu', 'equilibrio', 'compromiso', 'principios', 'mitos', 'ascenso', 
            'descenso', 'almas', 'unidad', 'hermandad', 'esfuerzo', 'mística', 'patria'
        }

        poema_epico_keywords = {
            'valentía', 'honor', 'hazañas', 'mitología', 'leyenda', 'versos', 'héroes', 
            'batallas', 'canto', 'protagonista', 'gloria', 'rivalidad', 'drama', 'épica', 
            'fuerza', 'retorno', 'origen', 'montañas', 'guerrero', 'herencia', 'imperio', 
            'realeza', 'juramento', 'destino', 'sacrificio', 'tradición', 'narrador', 
            'reinos', 'poder', 'adversidad', 'ley', 'cultura', 'río', 'tragedia', 
            'simbología', 'conflicto', 'lucha', 'unidad', 'compañerismo', 'profecía', 
            'viaje', 'triunfo', 'derrota', 'desafíos', 'aventura', 'supervivencia', 
            'arte', 'relatos', 'lírica', 'bravura', 'esperanza', 'fortaleza', 'ciudades', 
            'memoria', 'historia', 'libertad', 'juramentos', 'sabiduría', 'santos', 
            'guías', 'antigüedad', 'camino', 'luz', 'oscuridad', 'arquetipos', 'virtudes', 
            'morales', 'deseos', 'épico', 'consagración', 'campeón', 'armas', 'victoria', 
            'resistencia', 'fundadores', 'reyes', 'justicia', 'rituales', 'vínculos', 
            'humanidad', 'paradojas', 'místicas', 'oráculos', 'poesía', 'revelaciones', 
            'guías', 'renacer', 'enigma', 'trascendencia', 'aventuras', 'almas', 'civilizaciones', 
            'inmortalidad', 'visión', 'rutas'
        }

        romantic_keywords = {
            'princesa', 'castillo', 'amor', 'corazón', 'realeza', 'pasión', 'suspiros', 
            'miradas', 'caricias', 'besos', 'ternura', 'encuentro', 'secreto', 'galantería', 
            'poesía', 'alma', 'destino', 'luna', 'estrella', 'rosas', 'lágrimas', 'promesa', 
            'compañía', 'afecto', 'eternidad', 'versos', 'dulzura', 'fidelidad', 'deseo', 
            'magia', 'ensueño', 'melancolía', 'felicidad', 'fantasía', 'devoción', 
            'encanto', 'versos', 'compromiso', 'amistad', 'belleza', 'abrazos', 'música', 
            'esperanza', 'recuerdo', 'camino', 'sueños', 'infinito', 'romance', 'almas', 
            'historia', 'amanecer', 'atardecer', 'ternura', 'brillo', 'esperanza', 
            'delirio', 'ensueño', 'armas', 'inocencia', 'euforia', 'celebración', 'conquista', 
            'júbilo', 'fervor', 'ideal', 'estrellas', 'silencio', 'aliento', 'origen', 
            'confesión', 'cálido', 'susurros', 'plenitud', 'resplandor', 'refugio', 'poemas', 
            'comunión', 'eterno', 'compañía', 'devoción', 'adoración', 'unión', 'éxtasis'
        }

        horror_keywords = {
            'sangre', 'miedo', 'oscuridad', 'gritos', 'fantasma', 'sombras', 'monstruo', 
            'pesadilla', 'cráneo', 'terror', 'cadáver', 'tumba', 'venganza', 'muerto', 
            'pánico', 'cruel', 'abismo', 'desesperación', 'desolación', 'dolor', 'macabro', 
            'desgarrador', 'carne', 'cementerio', 'infierno', 'entierro', 'demonio', 
            'maldición', 'brujería', 'susurros', 'peligro', 'asesino', 'neblina', 'espanto', 
            'espeluznante', 'huesos', 'muñeca', 'mirada', 'almas', 'persecución', 'osario', 
            'llanto', 'ruinas', 'asesinato', 'horrendo', 'maldad', 'lobos', 'medieval', 
            'claustrofobia', 'ritual', 'maligno', 'destrucción', 'miedo', 'angustia', 
            'purgatorio', 'espíritus', 'guadaña', 'frialdad', 'sombrío', 'desafío', 'fobia', 
            'noche', 'estremecedor', 'pesadumbre', 'retorcido', 'misterio', 'engaño', 
            'cadenas', 'demencia', 'desgracia', 'trauma', 'locura', 'veneno', 'gritos', 
            'mitología', 'caza', 'secreto', 'siniestro', 'nocturno', 'terrorífico', 
            'delirio', 'silencio', 'despertar', 'vampiro', 'inquietante', 'temor', 'perdición', 
            'escalofríos', 'salvaje', 'monstruosidad', 'angustia', 'vacío', 'agonía'
        }

        terror_keywords = {
            'pánico', 'desesperación', 'sombra', 'monstruo', 'pesadilla', 'oscuro', 'grito', 
            'demonio', 'fobia', 'angustia', 'claustrofobia', 'abismo', 'susurro', 'tragedia', 
            'neblina', 'amenaza', 'aterrador', 'paranoia', 'prisión', 'laberinto', 'venganza', 
            'escapatoria', 'frenesí', 'perdición', 'pesadumbre', 'horror', 'fatalidad', 
            'silencio', 'oscuridad', 'vampiro', 'sombrío', 'manicomio', 'enigma', 'retorcido', 
            'agonía', 'inquietante', 'misterio', 'escapatoria', 'almas', 'niebla', 'muerte', 
            'maldición', 'vacío', 'delirio', 'desesperanza', 'castigo', 'asedio', 'infierno', 
            'desolación', 'tinieblas', 'destierro', 'destrucción', 'apocalipsis', 'temor', 
            'condena', 'maldad', 'cautiverio', 'susurros', 'frialdad', 'garras', 'osario', 
            'cadenas', 'renacimiento', 'sacrificio', 'muñeco', 'carroña', 'fantasmagórico', 
            'pérdida', 'locura', 'escapatoria', 'bestia', 'melancolía', 'lamentos', 'traición', 
            'rituales', 'aberración', 'horrendo', 'oculto', 'ensangrentado', 'aterrador', 
            'siniestro', 'desgracia', 'perdición', 'horroroso', 'veneno', 'sangriento', 
            'persecución', 'decadencia', 'gritos', 'sombras', 'tormento', 'vacío'
        }

        gothic_keywords = {
            'cementerio', 'melancolía', 'castillo', 'luz de luna', 'sombras', 'oscuridad', 
            'gárgolas', 'torres', 'niebla', 'misterio', 'lamentos', 'soledad', 'ventanas', 
            'candelabros', 'arcos', 'gótico', 'tumbas', 'elegancia', 'tormenta', 'susurros', 
            'antigüedad', 'rosas negras', 'reliquias', 'ecos', 'luto', 'techo abovedado', 
            'sepulcro', 'maldición', 'corredores', 'murciélagos', 'desamor', 'tristeza', 
            'piedras', 'relojes', 'sombrío', 'gótica', 'carillón', 'antorchas', 'misterioso', 
            'suspiros', 'eco', 'portones', 'vidrieras', 'gárgola', 'laberinto', 'frescos', 
            'sacrilegio', 'caballero', 'ruinas', 'tinieblas', 'soledad', 'templo', 
            'bóveda', 'torres altas', 'susurros', 'umbrales', 'medieval', 'clásico', 
            'poético', 'inmortalidad', 'piedra', 'capilla', 'puertas', 'luz tenue', 
            'estatuas', 'frialdad', 'arquitectura', 'templos', 'romanticismo', 'nostalgia', 
            'ventanas góticas', 'poesía', 'rosetón', 'capillas', 'catedral', 'bóvedas', 
            'figuras', 'rituales', 'hierro', 'tumbas', 'vidrio', 'esperanza', 'vínculos', 
            'resonancia', 'espejos', 'bóveda', 'vacío', 'ruinas', 'castillo'
        }

        cubist_keywords = {
            'fragmentos', 'perspectiva', 'formas', 'abstracción', 'geometría', 'ángulos', 
            'colores', 'estructura', 'figuras', 'descomposición', 'líneas', 'superficies', 
            'pintura', 'boceto', 'simetría', 'conceptual', 'visión', 'escala', 'módulos', 
            'planos', 'relieve', 'dinámica', 'texturas', 'simultaneidad', 'variaciones', 
            'composición', 'realidad', 'deconstrucción', 'arte', 'volumen', 'tonos', 
            'contraste', 'abstracciones', 'sombras', 'formas angulares', 'cambios', 
            'gráficos', 'representación', 'espacio', 'movimiento', 'diseño', 'simetría', 
            'arte moderno', 'líneas geométricas', 'bocetos', 'pintoresco', 'dibujo', 
            'relieve', 'complejidad', 'tamaño', 'bordes', 'dinamismo', 'visión angular', 
            'marcos', 'mundo abstracto', 'modelos', 'secciones', 'conceptualismo', 
            'formas planas', 'sombras abstractas', 'visión múltiple', 'tonalidad', 'escala', 
            'ángulos', 'constructivismo', 'multidimensional', 'diseño estructural', 
            'simultáneo', 'detalles', 'arquitectura', 'perspectiva angular', 'arte analítico', 
            'representación', 'formas divididas', 'volúmenes', 'vanguardia', 'análisis', 
            'contrastes', 'fases', 'mosaicos', 'gráficos angulares'
        }

        barroco_keywords = {
            'ornamento', 'contraste', 'detalles', 'dramático', 'exceso', 'lujo', 'reliquias', 
            'curvatura', 'cúpulas', 'relieves', 'dinamismo', 'majestuosidad', 'claroscuro', 
            'dorado', 'exuberancia', 'teatralidad', 'arquitectura', 'escultura', 'pintura', 
            'grandeza', 'religiosidad', 'misticismo', 'emoción', 'intrincado', 'virtuosidad', 
            'complejidad', 'adorno', 'sombras', 'reflejos', 'esplendor', 'movimiento', 
            'riqueza', 'pasión', 'materialidad', 'juegos de luces', 'grandes volúmenes', 
            'reales', 'colores vivos', 'tensión', 'detallismo', 'perspectiva', 'pliegues', 
            'ornamentación', 'contrastante', 'pomposo', 'majestad', 'gravedad', 'dinámico', 
            'naturalismo', 'idealismo', 'alegorías', 'formas', 'movimiento escultórico', 
            'laberíntico', 'luz celestial', 'figuras humanas', 'religión', 'estructuras', 
            'arcángeles', 'virgen', 'escultórico', 'elaboración', 'decoración', 'arte sacro', 
            'poesía barroca', 'teología', 'sentimientos', 'catedrales', 'templo', 
            'reyes', 'divinidad', 'iconografía', 'belleza', 'majestuosidad', 'emoción', 
            'pasión', 'dramatismo', 'complicado', 'épico', 'relieve artístico', 
            'geometría ornamental', 'espejos', 'simetría', 'esculturas', 'pinceladas'
        }
        
        words = set(content.lower().split())
        
        if words.intersection(romantic_keywords):
            return "Romántico"
        elif words.intersection(horror_keywords):
            return "Horror"
        elif words.intersection(epopeya_keywords):
            return "Epopeya"
        elif words.intersection(terror_keywords):
            return "Terror"
        elif words.intersection(gothic_keywords):
            return "Gotico"
        elif words.intersection(cubist_keywords):
            return "Cubista"
        elif words.intersection(barroco_keywords):
            return "Barroco"
        else:
            return "Desconocido"

class PoemAnalyzerApp:
    def __init__(self, root):
        self.analyzer = PoemAnalyzer()
        self.root = root
        #self.root.title("Analizador de Poemas con Sentence Trasformer")

        # Botón para cargar el corpus
        self.load_button = tk.Button(root, text="Cargar Corpus", command=self.load_corpus)
        self.load_button.pack(pady=10)

        # Entrada para la consulta
        self.query_label = tk.Label(root, text="Poema de Prueba:")
        self.query_label.pack()
        self.query_text = tk.Text(root, width=60, height=20)  # Aumentar ancho a 80 para mayor espacio
        self.query_text.pack(pady=10)

        # Botón para buscar poemas similares
        self.search_button = tk.Button(root, text="Calcular Similitud", command=self.search_poems)
        self.search_button.pack(pady=10)

        # Botón para limpiar poema de prueba
        self.clear_poem_button = tk.Button(root, text="Limpiar Poema de Prueba", command=self.clear_poem)
        self.clear_poem_button.pack(pady=5)

        # Botón para limpiar resultados
        self.clear_results_button = tk.Button(root, text="Limpiar Resultados", command=self.clear_results)
        self.clear_results_button.pack(pady=5)

        # Área de texto para mostrar los resultados
        self.results_text = scrolledtext.ScrolledText(root, height=20, width=80)
        self.results_text.pack(pady=10)

    def load_corpus(self):
        """Abre un diálogo para seleccionar y cargar el archivo del corpus."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            self.analyzer.load_corpus(file_path)
            messagebox.showinfo("Éxito", "Corpus cargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el corpus: {e}")

    def search_poems(self):
        """Busca poemas similares basados en la consulta ingresada."""
        #query = self.query_entry.get()
        query = self.query_text.get("1.0",tk.END).strip()
        if not query:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una consulta.")
            return

        try:
            results = self.analyzer.find_similar_poems(query, top_k=10)  # Cambiado a 10
            self.results_text.delete(1.0, tk.END)

            if results:
                for idx, result in enumerate(results):
                    line_number = result['line_number'] + 1 #Comienza despues de la descripcion de cada columna
                    classification_words = ', '.join(result['classification_words'])
                    genre_prediction = self.analyzer.predict_genre(result['content'])

                    # Mostrar resultados con palabras similares y predicción de género
                    self.results_text.insert(tk.END, f"{idx + 1}.- Autor: {result['author']}\n")
                    self.results_text.insert(tk.END, f"Título: {result['title']}\n")
                    #self.results_text.insert(tk.END, f"Contenido: {result['content']}\n")
                    self.results_text.insert(tk.END, f"Línea del Corpus: {line_number}\n")
                    self.results_text.insert(tk.END, f"Similitud: {result['similarity']:.4f}\n")
                    self.results_text.insert(tk.END, f"Género: {genre_prediction}\n")
                    #self.results_text.insert(tk.END, f"Palabras de clasificación: {classification_words}\n\n")
            else:
                self.results_text.insert(tk.END, "No se encontraron resultados similares.\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

    def clear_poem(self):
        """Limpia el campo de texto del poema."""
        # Limpiar campo de entrada del poema
        self.query_text.delete(1.0,tk.END)

    def clear_results(self):
        """Limpia el área de resultados."""
        self.results_text.delete(1.0, tk.END)  # Limpiar área de resultados

if __name__ == "__main__":
    root = tk.Tk()
    app = PoemAnalyzerApp(root)
    root.mainloop()
